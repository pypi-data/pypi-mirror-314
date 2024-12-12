import asyncio
from datetime import datetime, timedelta

from kelvin.application import KelvinApp
from kelvin.message.primitives import AssetDataMessage


async def on_asset_input(msg: AssetDataMessage):
    print(f"Received message timestamp={msg.timestamp} value={msg.payload}, asset={msg.resource.asset}")


async def main() -> None:
    # Creating instance of Kelvin App Client
    app = KelvinApp()
    # Set on_asset_input Callback
    app.on_asset_input = on_asset_input

    # Get current time as the start time of the window
    now = datetime.now()

    # Connect the App Client
    await app.connect()

    # Processing data using a 10 seconds hopping window with a 5 seconds hop size
    async for asset_name, df in app.hopping_window(
        window_size=timedelta(seconds=10), hop_size=timedelta(seconds=5)
    ).stream(now):
        print(asset_name, df)


if __name__ == "__main__":
    asyncio.run(main())
