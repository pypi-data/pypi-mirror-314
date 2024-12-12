import pytest
from pydantic.v1 import parse_obj_as

from kelvin.krn import *

KRNS = {
    "krn:app:smart-pcp": KRNApp,
    "krn:appversion:smart-pcp/2.0.0": KRNAppVersion,
    "krn:asset:air-conditioner-1": KRNAsset,
    "krn:ad:air-conditioner-1/temp-setpoint": KRNAssetDataStream,
    "krn:am:air-conditioner-1/temp-setpoint ": KRNAssetMetric,
    "krn:ap:air-conditioner-1/closed_loop": KRNAssetParameter,
    "krn:datastream:temp-setpoint": KRNDatastream,
    "krn:job:parameters-schedule-worker/1257897347822083": KRNJob,
    "krn:param:configuration.ip": KRNParameter,
    "krn:recommendation:86a425b4-b43f-4989-a38f-b18f6b3d1ec7": KRNRecommendation,
    "krn:schedule:6830a7d3-bcf3-4a64-8126-eaaeeca86676": KRNSchedule,
    "krn:srv-acc:node-client-my-edge-cluster": KRNServiceAccount,
    "krn:user:me@example.com": KRNUser,
    "krn:wl:my-node/temp-adjuster-1": KRNWorkload,
    "krn:wlappv:cluster_name/workload_name:app_name/app_version": KRNWorkloadAppVersion,
}


@pytest.mark.parametrize("krn,cls", KRNS.items())
def test_parse_krns(krn, cls):
    assert isinstance(KRN.from_string(krn), cls)


@pytest.mark.parametrize("krn,cls", KRNS.items())
def test_encode_krns(krn, cls):
    # skip special case, KRNAssetMetric is encoded as KRNAssetDataStream
    if cls == KRNAssetMetric:
        return

    assert KRN.from_string(krn).encode() == krn


def test_encode_krn_pydantic_v1():
    kr = parse_obj_as(KRN, "krn:ad:asset1/metric1")

    assert isinstance(kr, KRNAssetDataStream)
    assert kr.asset == "asset1"
    assert kr.data_stream == "metric1"
