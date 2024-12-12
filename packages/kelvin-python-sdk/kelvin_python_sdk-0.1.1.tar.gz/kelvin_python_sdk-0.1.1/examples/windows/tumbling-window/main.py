import asyncio
from datetime import datetime, timedelta

from kelvin.application import KelvinApp
from kelvin.message.primitives import AssetDataMessage


# on_asset_input Callback
async def on_asset_input(msg: AssetDataMessage):
    asset = msg.resource.asset
    value = msg.payload
    print(f"Received message timestamp={msg.timestamp} value={value}, asset: {asset}")


async def main() -> None:
    # Creating instance of Kelvin App Client
    app = KelvinApp()
    # Set on_asset_input Callback
    app.on_asset_input = on_asset_input

    # Get current time as the start time of the window
    now = datetime.now()

    # Connect the App Client
    await app.connect()

    # Streaming data in 10-seconds tumbling windows
    async for asset_name, df in app.tumbling_window(window_size=timedelta(seconds=10)).stream(now):
        print(asset_name, df)


if __name__ == "__main__":
    asyncio.run(main())
