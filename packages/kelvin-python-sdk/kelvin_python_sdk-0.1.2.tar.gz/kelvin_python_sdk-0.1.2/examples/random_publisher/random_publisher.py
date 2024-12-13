import asyncio
import random
from typing import Optional

from pydantic import BaseModel

from kelvin.application import KelvinApp
from kelvin.application.client import ResourceDatastream
from kelvin.krn import KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import Boolean, Message, Number, String
from kelvin.message.msg_type import KMessageTypePrimitive, PrimitiveTypes


class Config(BaseModel):
    model_config = {"extra": "allow"}

    period: float = 30
    min: float = 0
    max: float = 100
    random: bool = True


class RandomPublisher:
    app: KelvinApp
    config: Config
    msg_count: int
    metrics: list[ResourceDatastream]
    current_value: float

    def __init__(self, app: KelvinApp = KelvinApp()) -> None:
        self.app = app
        self.config = Config()
        self.msg_count = 0
        self.metrics = []
        self.current_value = 0

    async def connect(self) -> None:
        await self.app.connect()
        logger.debug(
            "App connected",
            config=self.app.app_configuration,
            assets=self.app.assets,
        )
        self.config = Config.model_validate(self.app.app_configuration)
        self.metrics = [r for asset in self.app.assets.values() for r in asset.datastreams.values()]
        print("Metrics: ", self.metrics)
        self.current_value = self.config.min

    def increment_current_value(self) -> None:
        if self.current_value >= self.config.max:
            self.current_value = self.config.min
        else:
            self.current_value += 1

    def build_message_from_resource(self, resource: ResourceDatastream) -> Optional[Message]:
        krn_ad = KRNAssetDataStream(resource.asset.asset, resource.datastream.name)
        if not isinstance(resource.datastream.type, KMessageTypePrimitive):
            return None

        if resource.datastream.type.primitive == PrimitiveTypes.boolean:
            return Boolean(resource=krn_ad, payload=random.choice([True, False]))

        number = (
            round(random.random() * (self.config.max - self.config.min) + self.config.min, 2)
            if self.config.random
            else self.current_value
        )

        if resource.datastream.type.primitive == PrimitiveTypes.number:
            return Number(resource=krn_ad, payload=number)

        if resource.datastream.type.primitive == PrimitiveTypes.string:
            return String(resource=krn_ad, payload=f"str_{number}")

        return None

    async def on_asset_input(self, msg: Message) -> None:
        logger.info("Received control change", resource=str(msg.resource), payload=msg.payload)
        await self.app.publish(Message(resource=msg.resource, payload=msg.payload, type=msg.type))

    async def publisher(self) -> None:
        while True:
            for metric in self.metrics:
                msg = self.build_message_from_resource(metric)
                if msg is not None:
                    ok = await self.app.publish(msg)
                    self.msg_count += int(ok)

            self.increment_current_value()
            await asyncio.sleep(self.config.period)

    async def publish_count_log(self) -> None:
        while True:
            logger.info(f"Published {self.msg_count} messages in the last minute")
            self.msg_count = 0
            await asyncio.sleep(60)

    async def run_forever(self) -> None:
        await self.connect()
        self.app.on_asset_input = self.on_asset_input

        t = {asyncio.create_task(self.publisher()), asyncio.create_task(self.publish_count_log())}

        await asyncio.gather(*t)


if __name__ == "__main__":
    app = RandomPublisher()
    asyncio.run(app.run_forever())
