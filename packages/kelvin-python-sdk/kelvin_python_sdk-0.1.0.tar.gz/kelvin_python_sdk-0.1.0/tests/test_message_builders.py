""" Test Message Builders """

import uuid
from datetime import datetime, timedelta

from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import ControlChange, ControlChangeMsg, DataTag, Recommendation, RecommendationMsg


def test_builder_control_change() -> None:
    now = datetime.now()

    cc = ControlChange(resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25)

    cc_msg = cc.to_message()

    assert isinstance(cc_msg, ControlChangeMsg)
    assert cc_msg.payload.expiration_date == cc.expiration_date
    assert cc_msg.payload.payload == cc.payload
    assert cc_msg.resource == cc.resource


def test_builder_recommendation() -> None:
    now = datetime.now()
    cc_uuid = uuid.uuid4()

    cc = ControlChange(
        resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25, control_change_id=cc_uuid
    )

    rec = Recommendation(
        resource=KRNAsset("asset1"),
        type="e2e_recommendation",
        control_changes=[cc],
        expiration_date=timedelta(minutes=5),
        metadata={"key": "value"},
        auto_accepted=True,
        custom_identifier="custom_id",
    )

    rec_msg = rec.to_message()
    assert rec_msg.payload.metadata == rec.metadata
    assert rec_msg.payload.custom_identifier == rec.custom_identifier
    assert isinstance(rec_msg, RecommendationMsg)


def test_builder_data_tag_minimum() -> None:
    now = datetime.now()
    tag_builder = DataTag(start_date=now, tag_name="tag1", resource=KRNAsset("asset1"))
    tag_msg = tag_builder.to_message()

    assert tag_msg.payload.start_date == now
    assert tag_msg.payload.end_date == now
    assert tag_msg.payload.tag_name == "tag1"
    assert tag_msg.resource == tag_msg.payload.resource == KRNAsset("asset1")


def test_builder_data_tag_all() -> None:
    start = datetime.now() - timedelta(minutes=5)
    end = datetime.now()
    tag_builder = DataTag(
        start_date=start,
        end_date=end,
        tag_name="tag1",
        resource=KRNAsset("asset1"),
        description="this is description",
        contexts=[KRNAssetDataStream("asset1", "metric1")],
    )
    tag_msg = tag_builder.to_message()

    assert tag_msg.payload.start_date == start
    assert tag_msg.payload.end_date == end
    assert tag_msg.payload.tag_name == "tag1"
    assert tag_msg.payload.description == "this is description"
    assert tag_msg.payload.contexts == [KRNAssetDataStream("asset1", "metric1")]
    assert tag_msg.resource == tag_msg.payload.resource == KRNAsset("asset1")
