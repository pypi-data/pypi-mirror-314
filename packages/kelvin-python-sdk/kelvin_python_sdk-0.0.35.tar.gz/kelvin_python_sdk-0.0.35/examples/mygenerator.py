import asyncio
from typing import AsyncGenerator

from kelvin.krn import KRNAssetDataStream
from kelvin.message import Number
from kelvin.publisher import DataGenerator, MessageData


class MyGenerator(DataGenerator):
    def __init__(self) -> None:
        print("Hello from MyGenerator")

    async def run(self) -> AsyncGenerator[MessageData, None]:
        print("Running MyGenerator")

        for i in range(10):
            yield MessageData(
                resource=KRNAssetDataStream("", "input-number"),
                timestamp=None,
                value=i,
            )
            await asyncio.sleep(1)


class OtherGenerator:
    def __init__(self) -> None:
        print("Hello from OtherGenerator")

    async def run(self) -> AsyncGenerator[Number, None]:
        print("Running OtherGenerator")
        for i in range(20, 30):
            yield Number(
                resource=KRNAssetDataStream("test-asset-1", "input-number"),
                payload=i,
            )
            await asyncio.sleep(1)
