"""Test Data Models."""

import json
from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel

from kelvin.krn import KRNAssetDataStream, KRNWorkload
from kelvin.message import (
    ControlChangeAck,
    ControlChangeMsg,
    ControlChangeStatus,
    KMessageTypeData,
    Message,
    Number,
    StateEnum,
    String,
)


class MyTypeModel(BaseModel):
    x: int = 123
    y: float = 2.1


class MyType(Message):
    TYPE_ = KMessageTypeData(icd="my.type")

    payload: MyTypeModel = MyTypeModel()


def test_create_messages() -> None:
    # Build message from Message with "type"
    time_before = datetime.now().astimezone()
    msg = Message.model_validate(
        {
            "type": "data;pt=string",
            "id": "78ab8516-70be-46c1-b97b-ddb31dfd25e4",
            "payload": "text value",
            "resource": "krn:ad:foo/bar",
        }
    )
    time_after = datetime.now().astimezone()

    assert isinstance(msg, String)
    assert isinstance(msg.timestamp, datetime)
    assert time_before < msg.timestamp < time_after
    assert msg.payload == "text value"
    assert msg.id == UUID("78ab8516-70be-46c1-b97b-ddb31dfd25e4")

    # Build a primitive message
    msg = Message.model_validate(
        {
            "type": "data;pt=number",
            "id": "78ab8516-70be-46c1-b97b-ddb31dfd25e4",
            "payload": 123.45,
            "resource": "krn:ad:foo/bar",
        }
    )

    assert isinstance(msg, Number)
    assert msg.payload == 123.45
    assert msg.id == UUID("78ab8516-70be-46c1-b97b-ddb31dfd25e4")

    # now a non data message
    msg = Message.model_validate(
        {
            "type": "control-status",
            "payload": {"state": "failed", "message": "Status is failed."},
        }
    )
    assert isinstance(msg, ControlChangeStatus)
    assert isinstance(msg.id, UUID)
    assert msg.payload.state == StateEnum.failed

    # now a primitive message
    msg = Message.model_validate(
        {
            "type": "control-status",
            "payload": {"state": "failed", "message": "Status is failed."},
        }
    )
    assert isinstance(msg, ControlChangeStatus)
    assert isinstance(msg.id, UUID)
    assert msg.payload.state == StateEnum.failed

    # now a custom message
    msg = Message.model_validate(
        {
            "type": "data;icd=my.type",
            "payload": {"x": 555, "y": 9.81},
        }
    )
    assert isinstance(msg, MyType)
    assert msg.payload.x == 555
    assert msg.payload.y == 9.81

    # Build message from specific type
    msg = String.model_validate(
        {
            "timestamp": "2023-04-12T01:22:33.000000Z",
            "payload": "text value",
            "resource": "krn:ad:foo/bar",
        }
    )

    assert isinstance(msg, String)
    assert msg.payload == "text value"
    expected_datetime = datetime(2023, 4, 12, 1, 22, 33, tzinfo=timezone.utc).astimezone()
    assert msg.timestamp == expected_datetime

    msg = Number.model_validate(
        {
            "payload": 3.14,
            "resource": "krn:ad:foo/bar",
        }
    )

    assert isinstance(msg, Number)
    assert msg.payload == 3.14

    # now a non data message
    msg = ControlChangeStatus.model_validate({"payload": {"state": "ready", "message": "Status is ready."}})
    assert isinstance(msg, ControlChangeStatus)
    assert msg.payload.state == StateEnum.ready

    # init insted of parse
    msg = Number(payload=3.14, resource=KRNAssetDataStream("foo", "bar"))
    assert msg.payload == 3.14

    msg = MyType(payload={"x": 555, "y": 9.81})
    assert isinstance(msg, MyType)
    assert msg.payload.x == 555
    assert msg.payload.y == 9.81


def test_create_messages_v1() -> None:
    msg = Message.model_validate(
        {
            "id": "78ab8516-70be-46c1-b97b-ddb31dfd25e4",
            "data_type": "raw.text",
            "timestamp": "2023-04-12T01:22:33.000000Z",
            "asset_name": "the_asset",
            "name": "the_metric",
            "source": "the_node/the_workload",
            "target": "the_node/the_workload",
            "payload": {"value": "value v1"},
        }
    )

    assert isinstance(msg, Message)
    assert msg.id == UUID("78ab8516-70be-46c1-b97b-ddb31dfd25e4")
    assert isinstance(msg.resource, KRNAssetDataStream)
    assert msg.resource.asset == "the_asset"
    assert msg.resource.data_stream == "the_metric"
    assert isinstance(msg.source, KRNWorkload)
    assert msg.source.node == "the_node"
    assert msg.source.workload == "the_workload"
    assert msg.payload == {"value": "value v1"}


def test_create_messages_v0() -> None:
    msg = Message.model_validate(
        {
            "_": {
                "id": "78ab8516-70be-46c1-b97b-ddb31dfd25e4",
                "type": "raw.text",
                "time_of_validity": 1652204512633696000,
                "asset_name": "the_asset",
                "name": "the_metric",
                "source": "the_node/the_workload",
                "target": "the_node/the_workload",
            },
            "value": "value v0",
        }
    )

    assert isinstance(msg, Message)
    assert msg.id == UUID("78ab8516-70be-46c1-b97b-ddb31dfd25e4")
    assert isinstance(msg.resource, KRNAssetDataStream)
    assert msg.resource.asset == "the_asset"
    assert msg.resource.data_stream == "the_metric"
    assert isinstance(msg.source, KRNWorkload)
    assert msg.source.node == "the_node"
    assert msg.source.workload == "the_workload"
    assert msg.payload == {"value": "value v0"}

    assert msg.timestamp.timestamp() == 1652204512633696000 / 1e9  # type: ignore


def test_encode() -> None:
    msg = Message.model_validate(
        {
            "type": "data;icd=raw.text",
            "id": "78ab8516-70be-46c1-b97b-ddb31dfd25e4",
            "trace_id": "756432b0-8773-4b73-96d3-046e63a75fc4",
            "timestamp": "2023-04-12T01:22:33.000001Z",
            "resource": "krn:am:the_asset/the_metric",
            "source": "krn:wl:the_node/the_workload",
            "payload": {
                "value": "the_value",
            },
        }
    )

    expected_json = '{"id":"78ab8516-70be-46c1-b97b-ddb31dfd25e4","type":"data;icd=raw.text","trace_id":"756432b0-8773-4b73-96d3-046e63a75fc4","source":"krn:wl:the_node/the_workload","timestamp":"2023-04-12T01:22:33.000001Z","resource":"krn:ad:the_asset/the_metric","payload":{"value":"the_value"}}'

    assert msg.json() == expected_json

    expected_encode = b'{"id":"78ab8516-70be-46c1-b97b-ddb31dfd25e4","type":"data;icd=raw.text","trace_id":"756432b0-8773-4b73-96d3-046e63a75fc4","source":"krn:wl:the_node/the_workload","timestamp":"2023-04-12T01:22:33.000001Z","resource":"krn:ad:the_asset/the_metric","payload":{"value":"the_value"}}'
    assert msg.encode() == expected_encode


def test_encode_decode() -> None:
    msg = MyType(payload={"x": 555, "y": 9.81}, resource=KRNAssetDataStream("the_asset", "the_metric"))

    data = msg.encode()

    decoded = Message.decode(data)

    assert decoded == msg


def test_load_unknown_message() -> None:
    """Test loading an unknown message."""
    try:
        Message(type="nope", payload="nope")
    except Exception as exc:
        assert False, f"exception not expected {exc}"


def test_encode_control_message() -> None:
    msg = ControlChangeMsg(
        id="89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        trace_id="78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        timestamp=datetime.fromtimestamp(0),
        source=KRNWorkload(node="node", workload="workload"),
        resource=KRNAssetDataStream("big_asset", "big_name"),
        payload={
            "expiration_date": datetime.fromtimestamp(0),
            "timeout": 60,
            "retries": 10,
            "payload": {"value": 25},
        },
    )

    msg_json = msg.encode()

    assert json.loads(msg_json) == {
        "id": "89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        "trace_id": "78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        "source": "krn:wl:node/workload",
        "timestamp": "1970-01-01T00:00:00.000000Z",
        "resource": "krn:ad:big_asset/big_name",
        "type": "control",
        "payload": {
            "timeout": 60,
            "retries": 10,
            "expiration_date": "1970-01-01T00:00:00.000000Z",
            "payload": {"value": 25},
        },
    }


def test_encode_control_status() -> None:
    msg = ControlChangeStatus(
        id="89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        trace_id="78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        timestamp=datetime.fromtimestamp(0),
        source=KRNWorkload(node="node", workload="workload"),
        resource=KRNAssetDataStream("big_asset", "big_name"),
        payload={"state": StateEnum.applied, "message": "status-msg"},
    )

    msg_json = msg.encode()

    assert json.loads(msg_json) == {
        "id": "89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        "trace_id": "78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        "source": "krn:wl:node/workload",
        "timestamp": "1970-01-01T00:00:00.000000Z",
        "resource": "krn:ad:big_asset/big_name",
        "type": "control-status",
        "payload": {
            "state": "applied",
            "message": "status-msg",
        },
    }


def test_encode_control_ack() -> None:
    msg = ControlChangeAck(
        id="89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        trace_id="78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        timestamp=datetime.fromtimestamp(0).astimezone(),
        source=KRNWorkload(node="node", workload="workload"),
        resource=KRNAssetDataStream("big_asset", "big_name"),
        payload={"state": StateEnum.applied, "message": "ack-msg"},
    )

    msg_json = msg.encode()
    msg_dict = {
        "id": "89ab8516-70be-46c1-b97b-ddb31dfd25e4",
        "trace_id": "78ab8516-70be-46c1-b97b-ddb31dfd25e5",
        "source": "krn:wl:node/workload",
        "timestamp": "1970-01-01T00:00:00.000000Z",
        "resource": "krn:ad:big_asset/big_name",
        "type": "control-ack",
        "payload": {
            "state": "applied",
            "message": "ack-msg",
        },
    }

    assert json.loads(msg_json) == msg_dict

    dec_msg = msg.model_validate(msg_dict)
    assert msg == dec_msg
