from kelvin.application import filters
from kelvin.application.filters import is_data_message
from kelvin.krn import KRNApp, KRNAssetDataStream
from kelvin.message import Number, NumberParameter


def test_is_data_message():
    assert is_data_message(Number(payload=1.0, resource=KRNAssetDataStream("foo", "bar")))
    assert is_data_message(NumberParameter(payload=1.0, resource=KRNAssetDataStream("foo", "bar"))) is False


# Test input_equals
def test_input_equals_with_correct_data_stream():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream1"), payload=1.0)
    filter_func = filters.input_equals("data_stream1")
    assert filter_func(msg) == True


def test_input_equals_with_incorrect_data_stream():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream2"), payload=1.0)
    filter_func = filters.input_equals("data_stream1")
    assert filter_func(msg) == False


def test_input_equals_with_list_and_correct_data_stream():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream1"), payload=1.0)
    filter_func = filters.input_equals(["data_stream1", "data_stream2"])
    assert filter_func(msg) == True


def test_input_equals_with_list_and_incorrect_data_stream():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream3"), payload=1.0)
    filter_func = filters.input_equals(["data_stream1", "data_stream2"])
    assert filter_func(msg) == False


# Test asset_equals
def test_asset_equals_with_correct_asset():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream1"), payload=1.0)
    filter_func = filters.asset_equals("asset1")
    assert filter_func(msg) == True


def test_asset_equals_with_incorrect_asset():
    msg = Number(resource=KRNAssetDataStream("asset2", "data_stream1"), payload=1.0)
    filter_func = filters.asset_equals("asset1")
    assert filter_func(msg) == False


def test_asset_equals_with_list_and_correct_asset():
    msg = Number(resource=KRNAssetDataStream("asset1", "data_stream1"), payload=1.0)
    filter_func = filters.asset_equals(["asset1", "asset3"])
    assert filter_func(msg) == True


def test_asset_equals_with_list_and_incorrect_asset():
    msg = Number(resource=KRNAssetDataStream("asset2", "data_stream1"), payload=1.0)
    filter_func = filters.asset_equals(["asset1", "asset3"])
    assert filter_func(msg) == False


def test_non_krn_asset_data_stream():
    msg = Number(resource=KRNApp(app="app"), payload=1.0)  # Incorrect type
    filter_func = filters.input_equals("data_stream1")
    assert filter_func(msg) == False

    filter_func = filters.asset_equals("asset1")
    assert filter_func(msg) == False
