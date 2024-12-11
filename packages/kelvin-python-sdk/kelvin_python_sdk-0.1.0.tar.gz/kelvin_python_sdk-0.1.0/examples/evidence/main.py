import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator

from kelvin.ai import RollingWindow
from kelvin.application import KelvinApp, filters
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import AssetDataMessage, ControlChange, Recommendation
from kelvin.message.evidences import LineChart


class EvidenceApp:
    app: KelvinApp

    def __init__(self, app: KelvinApp = KelvinApp()) -> None:
        self.app = app
        self.app.on_connect = self.on_connect
        self.app.on_disconnect = self.on_disconnect
        self.stream = self.app.stream_filter(filters.input_equals("input-temperature"))

    async def on_connect(self) -> None:
        logger.info("Hello, evidence app connected")

    async def on_disconnect(self) -> None:
        logger.info("Hello, evidence app disconnected")

    async def window_task(self, window: RollingWindow, stream: AsyncGenerator[AssetDataMessage, None]):
        async for message in stream:
            window.append(message)

            df = window.get_asset_df(message.resource.asset)
            temp_mean = df["input-temperature"].mean()
            message.resource.data_stream = "temperature-mean"
            message.payload = temp_mean
            window.append(message)

    async def check_window_task(self, window: RollingWindow):
        skip_rec = dict()
        while True:
            dfs = window.get_assets_dfs()
            for asset, df in dfs.items():
                temp_limit = self.app.assets[asset].parameters.get("temperature-limit")
                if temp_limit is None:
                    continue

                if df["input-temperature"].mean() < temp_limit:
                    continue

                now = datetime.now()
                skip = skip_rec.get(asset, datetime.min)
                if now < skip:
                    logger.debug("Skip recommendation")
                    continue

                data = [[ts.timestamp() * 1000, value] for ts, value in zip(df.index, df["input-temperature"])]
                data_mean = [[ts.timestamp() * 1000, value] for ts, value in zip(df.index, df["temperature-mean"])]
                linechart = LineChart(
                    title=f"Temperature {asset}",
                    x_axis={"type": "datetime", "title": {"text": "Date"}},
                    y_axis={
                        "title": {"text": "Temperature (°C)"},
                        "plotLines": [
                            {
                                "value": temp_limit,
                                "color": "red",
                                "dashStyle": "Solid",
                                "width": 2,
                                "label": {
                                    "text": f"Limit {temp_limit}°C",
                                    "align": "right",
                                    "style": {"color": "red"},
                                },
                            }
                        ],
                    },
                    series=[
                        {
                            "name": "Temperature",
                            "type": "line",
                            "data": data,
                        },
                        {
                            "name": "Temperature Mean",
                            "type": "line",
                            "data": data_mean,
                            "marker": {"enabled": False},
                        },
                    ],
                )

                auto_accept = self.app.assets[asset].parameters.get("auto_accept", False)

                rec = Recommendation(
                    resource=KRNAsset(asset),
                    type="decrease",
                    expiration_date=timedelta(minutes=10),
                    control_changes=[
                        ControlChange(
                            resource=KRNAssetDataStream(asset, "out-temperature-setpoint"),
                            expiration_date=timedelta(minutes=10),
                            payload=temp_limit - 5,
                        )
                    ],
                    evidences=[linechart],
                    auto_accepted=auto_accept,
                )

                logger.info("Publishing recommendation", asset=asset, limit=temp_limit, auto_accept=auto_accept)
                await self.app.publish(rec)
                skip_rec[asset] = now + timedelta(minutes=2)

            await asyncio.sleep(5)

    async def run_forever(self) -> None:
        await self.app.connect()
        self.window = RollingWindow(
            datastreams=["input-temperature"],
            max_window_duration=60,
            timestamp_rounding_interval=timedelta(seconds=1),
        )

        await asyncio.gather(
            self.window_task(self.window, self.stream),
            self.check_window_task(self.window),
        )


if __name__ == "__main__":
    app = EvidenceApp()
    asyncio.run(app.run_forever())
