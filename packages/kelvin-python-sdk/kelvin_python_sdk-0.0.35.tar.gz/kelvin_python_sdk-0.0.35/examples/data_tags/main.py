import asyncio
from datetime import datetime, timedelta

from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import DataTag


async def main() -> None:
    app = KelvinApp()
    await app.connect()
    logger.info("App connected successfully")

    assets = app.assets.keys()

    i = 0
    while True:
        now = datetime.now()
        for asset in assets:
            tag = DataTag(
                tag_name="test-tag",
                resource=KRNAsset(asset),
                start_date=now - timedelta(seconds=20),
                end_date=now,
                description=f"This is a test tag, i={i}",
                contexts=[KRNAssetDataStream(asset, "input1")],
            )
            await app.publish(tag)
            logger.debug(f"Published tag for asset {asset}")

        i += 1
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
