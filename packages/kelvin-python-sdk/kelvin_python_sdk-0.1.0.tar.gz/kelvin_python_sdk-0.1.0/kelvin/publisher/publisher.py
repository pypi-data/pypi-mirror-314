from __future__ import annotations

import asyncio
import csv
import random
import sys
from abc import ABC, abstractmethod
from asyncio import Queue, StreamReader, StreamWriter
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Tuple, Union

import arrow
from pydantic import ValidationError
from pydantic.dataclasses import dataclass

from kelvin.application.config import (
    AppConfig,
    AssetsEntry,
    BridgeAppConfig,
    ConfigurationError,
    KelvinAppConfig,
    Metric,
    ParameterDefinition,
)
from kelvin.application.stream import KelvinStreamConfig
from kelvin.krn import KRN, KRNAssetDataStream, KRNAssetParameter, KRNWorkloadAppVersion
from kelvin.message import (
    KMessageType,
    KMessageTypeControl,
    KMessageTypeData,
    KMessageTypeDataTag,
    KMessageTypeParameter,
    KMessageTypeRecommendation,
    Message,
)
from kelvin.message.base_messages import (
    ManifestDatastream,
    Resource,
    ResourceDatastream,
    RuntimeManifest,
    RuntimeManifestPayload,
)


def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    items: list = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, Dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class KelvinPublisherConfig(KelvinStreamConfig):
    model_config = {"env_prefix": "KELVIN_PUBLISHER_"}

    ip: str = "0.0.0.0"


class PublisherError(Exception):
    pass


class PublishServer:
    CYCLE_TIMEOUT_S = 0.25
    NODE = "test_node"
    WORKLOAD = "test_workload"

    app_config: AppConfig
    allowed_assets: Optional[list[str]] = None
    asset_params: dict[Tuple[str, str], Union[bool, float, str]] = {}

    on_message: Callable[[Message], None]
    write_queue: Queue[Message]

    def __init__(self, conf: AppConfig, generator: DataGenerator, replay: bool = False) -> None:
        self.app_config = conf
        if self.app_config.app.kelvin.assets:
            self.allowed_assets = [asset.name for asset in self.app_config.app.kelvin.assets]
        elif self.app_config.app.bridge.metrics_map:
            self.allowed_assets = list(set(metric.asset_name for metric in self.app_config.app.bridge.metrics_map))

        self.writer = None
        self.on_message = log_message
        self.write_queue = Queue()
        self.config = KelvinPublisherConfig()
        self.running = False
        self.generator = generator
        # replay re-runs generator if it returns
        self.replay = replay

    def update_param(self, asset: str, param: str, value: Union[bool, float, str]) -> None:
        """Sets an asset parameter.
        Empty asset ("") to change app default

        Args:
            asset (Optional[str]): asset name (empty ("") for fallback)
            param (str): param name
            value (Union[bool, float, str]): param value
        """
        self.asset_params[(asset, param)] = value

    def add_extra_assets(self, assets_extra: list[str]) -> None:
        self.allowed_assets = assets_extra

    def bridge_app_yaml_to_runtime(self, bridge: BridgeAppConfig) -> RuntimeManifest:
        asset_metrics_map: dict[str, Resource] = {}
        metric_datastream_map: dict[str, ManifestDatastream] = {}
        for metric in bridge.metrics_map:
            resource = asset_metrics_map.setdefault(metric.asset_name, Resource(type="asset", name=metric.asset_name))

            resource.datastreams[metric.name] = ResourceDatastream(
                map_to=metric.name, access=metric.access, owned=True, configuration=metric.configuration
            )

            metric_datastream_map.setdefault(
                metric.name, ManifestDatastream(name=metric.name, primitive_type_name=metric.data_type)
            )

        resources = list(asset_metrics_map.values())
        datastreams = list(metric_datastream_map.values())

        return RuntimeManifest(
            resource=KRNWorkloadAppVersion(
                node=self.NODE,
                workload=self.WORKLOAD,
                app=self.app_config.info.name,
                version=self.app_config.info.version,
            ),
            payload=RuntimeManifestPayload(
                resources=resources, configuration=bridge.configuration, datastreams=datastreams
            ),
        )

    def kelvin_app_yaml_to_runtime(self, kelvin: KelvinAppConfig, allowed_assets: list[str] | None) -> RuntimeManifest:
        if allowed_assets is None:
            allowed_assets = [asset.name for asset in kelvin.assets]

        manif_ds_map: dict[str, ManifestDatastream] = {}
        resource_ds_map: dict[str, ResourceDatastream] = {}

        for input in kelvin.inputs:
            ds_name = input.name
            owned = input.control_change
            access = "WO"

            resource_ds_map[ds_name] = ResourceDatastream(map_to=ds_name, access=access, owned=owned)
            manif_ds_map[ds_name] = ManifestDatastream(name=ds_name, primitive_type_name=input.data_type)

        for output in kelvin.outputs:
            ds_name = output.name
            owned = False
            access = "RO"

            resource_ds = resource_ds_map.setdefault(
                ds_name, ResourceDatastream(map_to=ds_name, access=access, owned=owned)
            )
            if resource_ds.access != access:
                resource_ds.access = "RW"

            manif_ds = manif_ds_map.setdefault(
                ds_name, ManifestDatastream(name=ds_name, primitive_type_name=output.data_type)
            )

            if manif_ds.primitive_type_name != output.data_type:
                raise ConfigurationError(f"data type mismatch for output {ds_name}")

        resources: List[Resource] = []
        for asset in allowed_assets:
            asset_params = {}
            for param in kelvin.parameters:
                payload = (
                    self.asset_params.get((asset, param.name))  # asset override
                    or self.asset_params.get(("", param.name))  # asset override default ("")
                    or next(  # asset parameter defined in configuration
                        (
                            asset.parameters.get(param.name, {}).get("value")
                            for asset in self.app_config.app.kelvin.assets
                            if asset.name == asset
                        ),
                        None,
                    )
                    or param.default.get("value", None)  # app defaults
                    if param.default
                    else None
                )

                if payload is None:
                    # asset has no parameter and parameter doesn't have default value
                    continue

                try:
                    if param.data_type == "number":
                        payload = float(payload)
                    elif param.data_type == "string":
                        payload = str(payload)
                    elif param.data_type == "boolean":
                        payload = str(payload).lower() in ["true", "1"]
                except ValueError:
                    continue

                asset_params[param.name] = payload

            asset_properties = next((a.properties for a in kelvin.assets if a.name == asset), {})
            resources.append(
                Resource(
                    type="asset",
                    name=asset,
                    parameters=asset_params,
                    properties=asset_properties,
                    datastreams=resource_ds_map,
                )
            )

        return RuntimeManifest(
            resource=KRNWorkloadAppVersion(
                node=self.NODE,
                workload=self.WORKLOAD,
                app=self.app_config.info.name,
                version=self.app_config.info.version,
            ),
            payload=RuntimeManifestPayload(
                resources=resources, configuration=kelvin.configuration, datastreams=list(manif_ds_map.values())
            ),
        )

    def build_config_message(self) -> RuntimeManifest:
        if self.app_config.app.type == "bridge":
            return self.bridge_app_yaml_to_runtime(self.app_config.app.bridge)
        elif self.app_config.app.type == "kelvin":
            return self.kelvin_app_yaml_to_runtime(self.app_config.app.kelvin, self.allowed_assets)
        else:
            raise ConfigurationError(f"invalid app type: {self.app_config.app.type}")

    async def start_server(self) -> None:
        server = await asyncio.start_server(self.new_client, self.config.ip, self.config.port, limit=self.config.limit)
        print(f"Publisher started. Listening on {self.config.ip}:{self.config.port}")

        async with server:
            await server.serve_forever()

    async def new_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        if self.running is True:
            writer.close()
            return

        print("Connected")
        self.running = True

        connection_tasks = {
            asyncio.create_task(self.handle_read(reader)),
            asyncio.create_task(self.handle_write(writer, self.write_queue)),
        }

        gen_task = asyncio.create_task(self.handle_generator(self.generator))
        try:
            config_msg = self.build_config_message()
            writer.write(config_msg.encode() + b"\n")
        except ConfigurationError as e:
            print("Configuration error:", e)
            writer.close()
            self.running = False

        try:
            await writer.drain()
        except ConnectionResetError:
            pass

        _, pending = await asyncio.wait(connection_tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        if not gen_task.done():
            gen_task.cancel()

        self.running = False
        print("Disconnected")

    async def handle_read(self, reader: StreamReader) -> None:
        while self.running:
            data = await reader.readline()
            if not len(data):
                break
            try:
                msg = Message.model_validate_json(data)
                self.on_message(msg)
            except Exception as e:
                print("error parsing message", e)

    async def handle_write(self, writer: StreamWriter, queue: Queue[Message]) -> None:
        while self.running and not writer.is_closing():
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=self.CYCLE_TIMEOUT_S)
            except asyncio.TimeoutError:
                continue

            writer.write(msg.encode() + b"\n")

            try:
                await writer.drain()
            except ConnectionResetError:
                pass

    async def handle_generator(self, generator: DataGenerator) -> None:
        first_run = True
        while first_run or self.replay:
            first_run = False
            async for data in generator.run():
                if isinstance(data, MessageData):
                    await self.publish_data(data)
                elif isinstance(data, Message):
                    await self.publish_unsafe(data)

    async def publish_unsafe(self, msg: Message) -> None:
        """Publish the message as is, do not validate it against the app configuration

        Args:
            msg (Message): message to publish
        """
        await self.write_queue.put(msg)

    async def publish_data(self, data: MessageData) -> bool:
        if self.allowed_assets is not None and data.resource.asset and data.resource.asset not in self.allowed_assets:
            print(f"error publishing: asset not allowed to app. asset={data.resource.asset}")
            return False

        # if data.asset is empty publish to all allowed_assets (if set)
        assets = [data.resource.asset] if data.resource.asset else self.allowed_assets
        if assets is None:
            print("error publishing to empty asset: no allowed assets set")
            return False

        if self.app_config.app.type == "kelvin":
            app_resource: Union[Metric, ParameterDefinition, None] = None
            msg_resource_builder: Optional[type[KRN]] = None
            try:
                # check is app input
                app_resource = next(i for i in self.app_config.app.kelvin.inputs if i.name == data.resource.data_stream)
                msg_type: KMessageType = KMessageTypeData(primitive=app_resource.data_type)
                msg_resource_builder = KRNAssetDataStream
            except StopIteration:
                try:
                    # check is app param
                    app_resource = next(
                        p for p in self.app_config.app.kelvin.parameters if p.name == data.resource.data_stream
                    )
                    msg_type = KMessageTypeParameter(primitive=app_resource.data_type)
                    msg_resource_builder = KRNAssetParameter
                except StopIteration:
                    app_resource = None
        else:
            try:
                app_resource = next(
                    Metric(name=m.name, data_type=m.data_type)
                    for m in self.app_config.app.bridge.metrics_map
                    if m.name == data.resource.data_stream
                )
                msg_type = KMessageTypeData(primitive=app_resource.data_type)
                msg_resource_builder = KRNAssetDataStream
            except StopIteration:
                app_resource = None

        if app_resource is None or msg_resource_builder is None:
            # invalid resource for this app
            print(f"error publishing: invalid resource to app. resource={data.resource!s}")
            return False

        for asset in assets:
            try:
                msg = Message(
                    type=msg_type,
                    timestamp=data.timestamp or datetime.now().astimezone(),
                    resource=msg_resource_builder(asset, data.resource.data_stream),
                )
                msg.payload = type(msg.payload)(data.value) if type(msg.payload) is not type(None) else data.value

                await self.write_queue.put(msg)
            except (ValidationError, ValueError):
                print(
                    (
                        "error publishing value: invalid value for resource."
                        f" resource={data.resource!s}, value={data.value}"
                    )
                )
        return True


def log_message(msg: Message) -> None:
    msg_log = ""
    if isinstance(msg.type, KMessageTypeData):
        msg_log = "Data "
    elif isinstance(msg.type, KMessageTypeControl):
        msg_log = "Control Change "
    elif isinstance(msg.type, KMessageTypeRecommendation):
        msg_log = "Recommendation "
    elif isinstance(msg.type, KMessageTypeDataTag):
        msg_log = "Data Tag "

    print(f"\nReceived {msg_log}Message:\n", repr(msg))


@dataclass
class MessageData:
    resource: KRNAssetDataStream
    timestamp: Optional[datetime]
    value: Any


@dataclass
class AppIO:
    name: str
    data_type: str
    asset: str


class DataGenerator(ABC):
    @abstractmethod
    async def run(self) -> AsyncGenerator[Union[MessageData, Message], None]:
        if False:
            yield  # trick for mypy


class CSVPublisher(DataGenerator):
    def __init__(
        self,
        csv_file_path: str,
        publish_interval: Optional[float] = None,
        playback: bool = False,
        ignore_timestamps: bool = False,
        now_offset: bool = False,
    ):
        csv.field_size_limit(sys.maxsize)
        self.csv_file_path = csv_file_path
        self.publish_rate = publish_interval
        self.playback = playback
        self.ignore_timestamps = ignore_timestamps
        self.now_offset = now_offset

        csv_file = open(self.csv_file_path)
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        self.csv_has_timestamp = "timestamp" in headers
        self.use_csv_timestamps = self.csv_has_timestamp and not self.ignore_timestamps

        if self.playback and not self.use_csv_timestamps:
            raise PublisherError("csv must have timestamp column to use csv timestamps")

    def parse_timestamp(self, ts_str: str, offset: timedelta = timedelta(0)) -> Optional[datetime]:
        try:
            timestamp = float(ts_str)
            return arrow.get(timestamp).datetime + offset
        except ValueError:
            pass

        try:
            return arrow.get(ts_str).datetime + offset
        except Exception as e:
            print(f"csv: error parsing timestamp. timestamp={ts_str}", e)
            return None

    async def run(self) -> AsyncGenerator[MessageData, None]:
        csv_file = open(self.csv_file_path)
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        last_timestamp = datetime.max

        ts_offset = timedelta(0)
        row = next(csv_reader)
        row_dict = dict(zip(headers, row))
        timestamp = datetime.now()
        row_ts_str = row_dict.pop("timestamp", "")

        if self.use_csv_timestamps:
            row_ts = self.parse_timestamp(row_ts_str)
            if row_ts is None:
                raise PublisherError(f"csv: invalid timestamp in first row. timestamp={row_ts_str}")

            if self.now_offset:
                ts_offset = timestamp.astimezone() - row_ts.astimezone()

            timestamp = row_ts + ts_offset

        asset = row_dict.pop("asset", "")
        for r, v in row_dict.items():
            if not v:
                continue
            yield MessageData(resource=KRNAssetDataStream(asset, r), value=v, timestamp=timestamp)
        last_timestamp = timestamp
        if self.publish_rate:
            await asyncio.sleep(self.publish_rate)

        for row in csv_reader:
            row_dict = dict(zip(headers, row))
            asset = row_dict.pop("asset", "")

            row_ts_str = row_dict.pop("timestamp", "")
            parsed_ts = self.parse_timestamp(row_ts_str, ts_offset) if self.use_csv_timestamps else datetime.now()
            if parsed_ts is None:
                print("csv: skipping row", row_dict)
                continue
            timestamp = parsed_ts

            if self.playback:
                # wait time between rows
                wait_time = max((timestamp.astimezone() - last_timestamp.astimezone()).total_seconds(), 0)
                last_timestamp = timestamp
                await asyncio.sleep(wait_time)

            for r, v in row_dict.items():
                if not v:
                    continue
                yield MessageData(resource=KRNAssetDataStream(asset, r), value=v, timestamp=timestamp)

            if self.publish_rate:
                await asyncio.sleep(self.publish_rate)

        if self.playback and wait_time > 0:
            # wait same time as last row, before replay
            await asyncio.sleep(wait_time)

        print("\nCSV ingestion is complete")


class Simulator(DataGenerator):
    app_yaml: str
    app_config: AppConfig
    rand_min: float
    rand_max: float
    random: bool
    current_value: float
    assets: list[AssetsEntry]
    params_override: dict[str, Union[bool, float, str]]

    def __init__(
        self,
        app_config: AppConfig,
        period: float,
        rand_min: float = 0,
        rand_max: float = 100,
        random: bool = True,
        assets_extra: list[str] = [],
        parameters_override: list[str] = [],
    ):
        self.app_config = app_config
        self.period = period
        self.rand_min = rand_min
        self.rand_max = rand_max
        self.random = random
        self.current_value = self.rand_min - 1
        self.params_override: dict[str, Union[bool, float, str]] = {}

        for override in parameters_override:
            param, value = override.split("=", 1)
            self.params_override[param] = value

        if len(assets_extra) > 0:
            self.assets = [AssetsEntry(name=asset, parameters={}) for asset in assets_extra]
        elif self.app_config.app.kelvin.assets:
            self.assets = self.app_config.app.kelvin.assets

    def generate_random_value(self, data_type: str) -> Union[bool, float, str, dict]:
        if data_type == "boolean":
            return random.choice([True, False])

        if self.random:
            number = round(random.random() * (self.rand_max - self.rand_min) + self.rand_min, 2)
        else:
            if self.current_value >= self.rand_max:
                self.current_value = self.rand_min
            else:
                self.current_value += 1
            number = self.current_value

        if data_type == "number":
            return number

        if data_type == "string":
            return f"str_{number}"

        if data_type == "object":
            return {"key": number}

        # should not reach here
        return ""

    async def run(self) -> AsyncGenerator[MessageData, None]:
        app_inputs: list[AppIO] = []
        if self.app_config.app.type == "kelvin":
            for asset in self.assets:
                for app_input in self.app_config.app.kelvin.inputs:
                    app_inputs.append(AppIO(name=app_input.name, data_type=app_input.data_type, asset=asset.name))

        elif self.app_config.app.type == "bridge":
            app_inputs = [
                AppIO(name=metric.name, data_type=metric.data_type, asset=metric.asset_name)
                for metric in self.app_config.app.bridge.metrics_map
                if metric.access == "RW"
            ]

        while True:
            for i in app_inputs:
                yield MessageData(
                    resource=KRNAssetDataStream(i.asset, i.name),
                    value=self.generate_random_value(i.data_type),
                    timestamp=None,
                )

            await asyncio.sleep(self.period)
