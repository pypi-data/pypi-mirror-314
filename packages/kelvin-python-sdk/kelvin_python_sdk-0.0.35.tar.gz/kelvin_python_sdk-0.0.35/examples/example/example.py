from __future__ import annotations

import asyncio
import random
from asyncio import Queue
from datetime import datetime, timedelta
from pprint import pprint
from typing import AsyncGenerator, Optional

from kelvin.application import AssetInfo, KelvinApp, filters
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import (
    AssetDataMessage,
    Boolean,
    ControlAck,
    ControlChange,
    Number,
    Recommendation,
    StateEnum,
    String,
)


class ExampleApp:
    app: KelvinApp

    def __init__(self, app: KelvinApp = KelvinApp()) -> None:
        self.app = app
        self.app.on_connect = self.on_connect
        self.app.on_disconnect = self.on_disconnect
        self.app.on_asset_change = self.on_asset_change
        self.app.on_app_configuration = self.on_app_configuration
        self.app.on_control_change = self.on_control_change

    async def on_connect(self) -> None:
        """Callback when the app is connected to the Kelvin Network."""
        print("Hello, it's connected")

    async def on_disconnect(self) -> None:
        """Callback when the app is disconnected from the Kelvin Network."""
        print("Hello, it's disconnected")

    async def on_control_change(self, cc: AssetDataMessage) -> None:
        """Callback when a Control Change is received."""
        print("Received Control Change: ", cc)
        await self.app.publish(
            ControlAck(resource=cc.resource, state=StateEnum.applied, message="CC app example applied cc")
        )

    async def on_asset_change(self, new: Optional[AssetInfo], old: Optional[AssetInfo]) -> None:
        """Callback when an asset is added, removed or changed from the Kelvin Network.

        The changed asset is received as argument.
        An empty AssetInfo(name="asset-name") is received when the asset is removed.
        """
        if new is None:
            print("Asset removed: ", old)
            return

        print("Asset change: ", new)

    async def on_app_configuration(self, conf: dict) -> None:
        """Callback when the app configuration is changed.
        The new configuration is received as argument."""
        print("App configuration change: ", conf)

    async def example_message_filter(self, queue: Queue[Number]) -> None:
        while True:
            msg = await queue.get()
            print("Received Input: ", msg)

            await self.app.publish(
                Number(resource=KRNAssetDataStream(msg.resource.asset, "output-number"), payload=msg.payload * 2)
            )

    async def example_message_stream(self, stream: AsyncGenerator[String, None]) -> None:
        async for msg in stream:
            print("Received Input: ", msg)

    async def publisher_task(self) -> None:
        while True:
            random_value = round(random.random() * 10, 2)

            # Publish Data (Number)
            await self.app.publish(
                Number(resource=KRNAssetDataStream("asset1", "output-random-number"), payload=random_value)
            )

            # Publish Data (String)
            await self.app.publish(
                String(resource=KRNAssetDataStream("asset1", "output-random-string"), payload=str(random_value))
            )

            # Publish Data (Boolean)
            await self.app.publish(
                Boolean(
                    resource=KRNAssetDataStream("asset1", "output-random-boolean"), payload=random.choice([True, False])
                )
            )

            expiration_date = datetime.now() + timedelta(minutes=10)

            # Publish Control Change
            await self.app.publish(
                ControlChange(
                    expiration_date=expiration_date,
                    resource=KRNAssetDataStream("asset1", "output-cc-number"),
                    payload=random_value,
                )
            )

            # Publish Recommendation
            await self.app.publish(
                Recommendation(
                    type="generic",
                    resource=KRNAsset("asset1"),
                    expiration_date=timedelta(minutes=10),
                    control_changes=[
                        ControlChange(
                            resource=KRNAssetDataStream("asset1", "output-cc-number"),
                            expiration_date=expiration_date,
                            retries=0,
                            timeout=300,
                            payload=random_value + 1,
                        )
                    ],
                )
            )
            await asyncio.sleep(2)

    async def run_forever(self) -> None:
        my_message_filter = self.app.filter(filters.input_equals("input-number"))
        my_message_stream = self.app.stream_filter(filters.input_equals("input-string"))

        await self.app.connect()
        logger.info("App Inputs")
        pprint(self.app.inputs)
        logger.info("App Outputs")
        pprint(self.app.outputs)
        logger.info("App Configuration")
        pprint(self.app.app_configuration)
        logger.info(f"App Assets ({len(self.app.assets)})")
        pprint(self.app.assets)

        await asyncio.gather(
            asyncio.create_task(self.example_message_filter(my_message_filter)),
            asyncio.create_task(self.example_message_stream(my_message_stream)),
            asyncio.create_task(self.publisher_task()),
        )


if __name__ == "__main__":
    app = ExampleApp()
    asyncio.run(app.run_forever())
