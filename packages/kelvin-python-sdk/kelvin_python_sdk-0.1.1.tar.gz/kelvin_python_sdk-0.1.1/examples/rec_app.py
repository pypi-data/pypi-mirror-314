import asyncio
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.krn import KRNAppVersion, KRNAsset, KRNAssetDataStream, KRNAssetParameter
from kelvin.message import AssetParameter, AssetParameters, ControlChange, Recommendation


async def main():
    app = KelvinApp()

    await app.connect()
    print("connected")
    while True:
        await app.publish(
            ControlChange(
                resource=KRNAssetDataStream("asset1", "output-cc-number"),
                expiration_date=timedelta(minutes=1),
                payload=255,
            )
        )
        await app.publish(
            Recommendation(
                resource=KRNAsset("asset1"),
                type="generic",
                control_changes=[
                    ControlChange(
                        resource=KRNAssetDataStream("asset1", "output-cc-number"),
                        expiration_date=timedelta(minutes=1),
                        payload=255,
                        timeout=5,
                        retries=5,
                    )
                ],
                auto_accepted=True,
            )
        )
        p1 = AssetParameter(resource=KRNAssetParameter("asset1", "password"), value="hunter2")
        await app.publish(AssetParameters(parameters=[p1]))

        p2 = AssetParameter(resource=KRNAssetParameter("asset1", "enabled"), value=True)
        p3 = AssetParameter(resource=KRNAssetParameter("asset1", "id"), value=1337)

        p4 = AssetParameter(resource=KRNAssetParameter("asset2", "password"), value="hunter2", comment="ganda comment")
        p5 = AssetParameter(resource=KRNAssetParameter("asset2", "enabled"), value=True)
        p6 = AssetParameter(resource=KRNAssetParameter("asset2", "id"), value=1337)

        pp = AssetParameters(resource=KRNAppVersion(app="bigapp", version="1.1.1"), parameters=[p1, p2, p3, p4, p5, p6])
        await app.publish(pp)

        pp2 = AssetParameters(parameters=[p1, p2, p3, p4, p5, p6])
        await app.publish(pp2)
        print("CCS done")

        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
