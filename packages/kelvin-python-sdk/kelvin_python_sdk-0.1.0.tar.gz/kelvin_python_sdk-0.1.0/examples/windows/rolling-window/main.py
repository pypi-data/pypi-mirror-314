import asyncio

from kelvin.application import KelvinApp
from kelvin.message.primitives import AssetDataMessage


# on_asset_input Callback
async def on_asset_input(msg: AssetDataMessage):
    asset = msg.resource.asset
    value = msg.payload
    print(f"Received message timestamp={msg.timestamp} value={value} asset: {asset}")


async def main() -> None:
    # Creating instance of Kelvin App Client
    app = KelvinApp()
    # Set on_asset_input Callback
    app.on_asset_input = on_asset_input
    # Connect the App Client
    await app.connect()

    # Processing data using a 5-minute hopping window with a 2-minute hop size
    async for asset_name, df in app.rolling_window(count_size=3).stream():
        print(asset_name, df)


if __name__ == "__main__":
    asyncio.run(main())
