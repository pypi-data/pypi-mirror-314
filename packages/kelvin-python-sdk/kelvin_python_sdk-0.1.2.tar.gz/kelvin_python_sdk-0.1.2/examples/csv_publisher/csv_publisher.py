from __future__ import annotations

import asyncio
from typing import Optional

import yaml
from pydantic import BaseModel

from kelvin.application import KelvinApp
from kelvin.krn import KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import Boolean, Message, Number, String
from kelvin.publisher.publisher import AppConfig, CSVPublisher, MessageData, Metric


def message_from_message_data(data: MessageData, outputs: list[Metric]) -> Optional[Message]:
    output = next((output for output in outputs if output.name == data.resource), None)
    if output is None:
        logger.error("csv metric not found in outputs", metric=data.resource)
        return None

    data_type = output.data_type
    if data_type == "boolean":
        msg_type = Boolean
        value = bool(data.value)
    elif data_type == "number":
        msg_type = Number
        value = float(data.value)
    elif data_type == "string":
        msg_type = String
        value = str(data.value)
    else:
        return None

    return msg_type(resource=KRNAssetDataStream(data.asset, data.resource), payload=value)


class AppConfiguration(BaseModel):
    model_config = {"extra": "allow"}

    csv: str
    replay: bool = False


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    assets = list(app.assets.keys())
    custom_config = AppConfiguration.model_validate(app.app_configuration)
    publisher = CSVPublisher(custom_config.csv, None, True)

    first_run = True
    while first_run or custom_config.replay:
        first_run = False
        async for data in publisher.run():
            for asset in assets:
                data.asset = asset
                msg = message_from_message_data(data, app.outputs)
                if msg is not None:
                    await app.publish(msg)


if __name__ == "__main__":
    asyncio.run(main())
