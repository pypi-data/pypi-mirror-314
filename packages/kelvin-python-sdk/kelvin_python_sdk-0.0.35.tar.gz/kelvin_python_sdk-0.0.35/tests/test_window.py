import asyncio
from datetime import datetime, timedelta

import pandas as pd
import pytest

from kelvin.application.window import BaseWindow, HoppingWindow, RollingWindow, TumblingWindow, round_nearest_time
from kelvin.krn import KRNAssetDataStream
from kelvin.message import Number


# Aux functions
def log_window(window: BaseWindow, asset: str, df: pd.DataFrame):

    df_stored = window.get_df(asset_name=asset)

    print("\n================BEGIN================")
    print(f"# ASSET: {asset}")
    print(f"\n# STORED:")
    if df_stored.empty:
        print("Empty dataframe")
    else:
        print(df_stored.head(20))
    print("\n# WINDOW:")
    if df.empty:
        print("Empty dataframe")
    else:
        print(df.head(20))
    print("================END================")


async def anext(ait):
    return await ait.__anext__()


# Test Timestamp Rounding
@pytest.mark.parametrize(
    "input_time, rounding, expected_time",
    [
        (datetime(2023, 9, 9, 12, 34, 56), timedelta(minutes=15), datetime(2023, 9, 9, 12, 30)),
        (datetime(2023, 9, 9, 12, 37, 30), timedelta(minutes=15), datetime(2023, 9, 9, 12, 30)),
        (datetime(2023, 9, 9, 23, 59, 30), timedelta(minutes=30), datetime(2023, 9, 10, 0, 0)),
        (datetime(2023, 9, 9, 0, 7, 30), timedelta(minutes=15), datetime(2023, 9, 9, 0, 0)),
        (datetime(2023, 9, 9, 12, 34, 56), timedelta(hours=1), datetime(2023, 9, 9, 13, 0)),
        (datetime(2023, 9, 9, 12, 29, 30), timedelta(hours=1), datetime(2023, 9, 9, 12, 0)),
        (datetime(2023, 9, 9, 12, 0, 0), None, datetime(2023, 9, 9, 12, 0, 0)),
    ],
)
def test_round_nearest_time(input_time, rounding, expected_time):
    assert round_nearest_time(input_time, rounding) == expected_time


# Test Tumbling Window
@pytest.mark.asyncio
async def test_tumbling_window():

    # Create window
    queue = asyncio.Queue()
    window = TumblingWindow(
        assets=["asset_01"], datastreams=["temperature"], queue=queue, window_size=timedelta(seconds=5), round_to=None
    )

    # Insert data into the queue
    now = datetime.now()
    for i in range(-5, 13):
        await queue.put(
            Number(
                resource=KRNAssetDataStream("asset_01", "temperature"), payload=i, timestamp=now + timedelta(seconds=i)
            )
        )

    # Get the stream
    stream = window.stream()

    # Assert first window
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert len(df) == 5
    assert df.index[0] == now + timedelta(seconds=1)
    assert df.index[-1] == now + timedelta(seconds=5)

    # Assert second window
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert len(df) == 5
    assert df.index[0] == now + timedelta(seconds=6)
    assert df.index[-1] == now + timedelta(seconds=10)

    # Assert third window
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert len(df) == 2
    assert df.index[0] == now + timedelta(seconds=11)
    assert df.index[-1] == now + timedelta(seconds=12)

    # Assert empty window
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert df.empty


@pytest.mark.asyncio
async def test_tumbling_window_out_of_order_timestamps():
    queue = asyncio.Queue()
    window = TumblingWindow(
        assets=["asset_01"], datastreams=["temperature"], queue=queue, window_size=timedelta(seconds=5), round_to=None
    )

    now = datetime.now()
    times = [now + timedelta(seconds=i) for i in [5, 1, 3, 4, 2]]
    for t in times:
        await queue.put(Number(resource=KRNAssetDataStream("asset_01", "temperature"), payload=1, timestamp=t))

    stream = window.stream()
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert df.index.is_monotonic_increasing


@pytest.mark.asyncio
async def test_tumbling_window_zero_size():
    queue = asyncio.Queue()
    with pytest.raises(ValueError, match="window_size must be a positive timedelta"):
        TumblingWindow(
            assets=["asset_01"],
            datastreams=["temperature"],
            queue=queue,
            window_size=timedelta(seconds=0),
            round_to=None,
        )


@pytest.mark.asyncio
async def test_tumbling_window_negative_size():
    queue = asyncio.Queue()
    with pytest.raises(ValueError, match="window_size must be a positive timedelta"):
        TumblingWindow(
            assets=["asset_01"],
            datastreams=["temperature"],
            queue=queue,
            window_size=timedelta(seconds=-5),
            round_to=None,
        )


@pytest.mark.asyncio
async def test_tumbling_window_zero_round_to():
    queue = asyncio.Queue()
    with pytest.raises(ValueError, match="round_to must be a positive timedelta instance or None"):
        TumblingWindow(
            assets=["asset_01"],
            datastreams=["temperature"],
            queue=queue,
            window_size=timedelta(seconds=-5),
            round_to=timedelta(),
        )


@pytest.mark.asyncio
async def test_tumbling_window_multiple_assets():
    queue = asyncio.Queue()
    window = TumblingWindow(
        assets=["asset_01", "asset_02"],
        datastreams=["temperature", "humidity"],
        queue=queue,
        window_size=timedelta(seconds=5),
        round_to=None,
    )

    now = datetime.now()
    for i in range(10):
        await queue.put(
            Number(
                resource=KRNAssetDataStream("asset_01", "temperature"), payload=i, timestamp=now + timedelta(seconds=i)
            )
        )
        await queue.put(
            Number(resource=KRNAssetDataStream("asset_02", "humidity"), payload=i, timestamp=now + timedelta(seconds=i))
        )

    stream = window.stream()
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert len(df) == 5

    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_02"
    assert len(df) == 5


@pytest.mark.asyncio
async def test_tumbling_window_high_frequency_data():
    queue = asyncio.Queue()
    window = TumblingWindow(
        assets=["asset_01"], datastreams=["temperature"], queue=queue, window_size=timedelta(seconds=1), round_to=None
    )

    now = datetime.now()
    for i in range(1, 4):
        # Simulating multiple data points at the exact same second
        for j in range(3):  # Three entries per second
            await queue.put(
                Number(
                    resource=KRNAssetDataStream("asset_01", "temperature"),
                    payload=j,
                    timestamp=now + timedelta(seconds=i),
                )
            )

    stream = window.stream()

    for i in range(1, 4):
        asset, df = await anext(stream)
        log_window(window=window, asset=asset, df=df)
        assert asset == "asset_01"
        assert len(df) == 1
        assert df.index[0] == now + timedelta(seconds=i)


# Test Hopping Window
@pytest.mark.asyncio
async def test_hopping_window():
    """Test the behavior of HoppingWindow with overlapping windows."""

    # Initialize the window parameters
    queue = asyncio.Queue()
    window = HoppingWindow(
        assets=["asset_01"],
        datastreams=["temperature"],
        queue=queue,
        window_size=timedelta(seconds=5),
        hop_size=timedelta(seconds=2),
        round_to=None,
    )

    # Insert test data into the queue
    now = datetime.now()
    data_points = [
        Number(
            resource=KRNAssetDataStream("asset_01", "temperature"),
            payload=i,
            timestamp=now + timedelta(seconds=i),
        )
        for i in range(-5, 13)
    ]
    for data_point in data_points:
        await queue.put(data_point)

    # Start the window stream
    stream = window.stream()

    # Define expected results for each window
    expected_windows = [
        (1, 5),
        (3, 7),
        (5, 9),
        (7, 11),
        (9, 12),
        (11, 12),
    ]

    for start, end in expected_windows:
        asset, df = await anext(stream)
        log_window(window=window, asset=asset, df=df)
        assert asset == "asset_01"
        expected_length = end - start + 1
        assert len(df) == expected_length, f"Expected {expected_length} rows, got {len(df)}"
        assert df.index[0] == now + timedelta(
            seconds=start
        ), f"Expected start index {now + timedelta(seconds=start)}, got {df.index[0]}"
        assert df.index[-1] == now + timedelta(
            seconds=end
        ), f"Expected end index {now + timedelta(seconds=end)}, got {df.index[-1]}"

    # Check the empty window at the end
    asset, df = await anext(stream)
    log_window(window=window, asset=asset, df=df)
    assert asset == "asset_01"
    assert df.empty, "Expected the final window to be empty."


# Test Rolling Window
@pytest.mark.asyncio
async def test_rolling_window():

    # Create window
    queue = asyncio.Queue()
    window = RollingWindow(assets=["asset_01"], datastreams=["temperature"], queue=queue, count_size=5, round_to=None)

    # Insert data into the queue
    now = datetime.now()
    for i in range(1, 16):
        await queue.put(
            Number(
                resource=KRNAssetDataStream("asset_01", "temperature"), payload=i, timestamp=now + timedelta(seconds=i)
            )
        )

    # Get the stream
    stream = window.stream()

    # Assert windows
    for i in range(1, 12):  # Rolling windows start from the first element
        asset, df = await anext(stream)
        log_window(window=window, asset=asset, df=df)
        assert asset == "asset_01", f"Expected asset 'asset_01', got {asset}"
        assert len(df) == 5, f"Expected window size of 5, got {len(df)}"
        assert df.index[0] == now + timedelta(
            seconds=i
        ), f"Expected start index {now + timedelta(seconds=i)}, got {df.index[0]}"
        assert df.index[-1] == now + timedelta(
            seconds=i + 4
        ), f"Expected end index {now + timedelta(seconds=i + 4)}, got {df.index[-1]}"
