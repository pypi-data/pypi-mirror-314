from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, field_serializer
from typing_extensions import Literal

from kelvin.krn import KRN, KRNAsset
from kelvin.message.evidences import BaseEvidence
from kelvin.message.message import Message
from kelvin.message.msg_type import (
    KMessageTypeControl,
    KMessageTypeControlAck,
    KMessageTypeControlStatus,
    KMessageTypeData,
    KMessageTypeDataTag,
    KMessageTypeParameters,
    KMessageTypeRecommendation,
    KMessageTypeRuntimeManifest,
)
from kelvin.message.utils import to_rfc3339_timestamp


class ValuePoint(BaseModel):
    value: Any
    timestamp: datetime
    source: Optional[str] = None


class ControlChangePayload(BaseModel):
    timeout: Optional[int] = Field(None, description="Timeout for retries")
    retries: Optional[int] = Field(None, description="Max retries")
    expiration_date: datetime = Field(description="Absolute expiration Date in UTC")
    payload: Any = Field(None, description="Control Change payload")

    from_value: Optional[ValuePoint] = Field(
        None, description="Optional value of the datastream at the moment of the creation", alias="from"
    )

    @field_serializer("expiration_date")
    def serialize_timestamp(self, ts: datetime) -> str:
        return to_rfc3339_timestamp(ts)


class ControlChangeMsg(Message):
    """Generic Control Change Message"""

    TYPE_ = KMessageTypeControl()

    payload: ControlChangePayload


class StateEnum(str, Enum):
    ready = "ready"
    sent = "sent"
    failed = "failed"
    processed = "processed"
    applied = "applied"
    rejected = "rejected"


class ReportedValues(BaseModel):
    before: Optional[ValuePoint] = None
    after: Optional[ValuePoint] = None


class ControlChangeStatusPayload(BaseModel):
    state: StateEnum
    message: Optional[str] = None
    reported: Optional[ReportedValues] = None

    # not used anymore, kept to avoid breaks
    payload: Optional[Any] = Field(None, description="Metric value at status time")


class ControlChangeStatus(Message):
    """Control Change Status"""

    TYPE_ = KMessageTypeControlStatus()

    payload: ControlChangeStatusPayload


class ControlChangeAck(Message):
    """Control Change Ack"""

    TYPE_ = KMessageTypeControlAck()

    payload: ControlChangeStatusPayload


class SensorDataPayload(BaseModel):
    data: List[float] = Field(..., description="Array of sensor measurements.", min_length=1)
    sample_rate: float = Field(..., description="Sensor sample-rate in Hertz.", gt=0.0)


class SensorDataMsg(Message):
    """Sensor data."""

    TYPE_ = KMessageTypeData("object", "kelvin.sensor_data")

    payload: SensorDataPayload


class RecommendationControlChange(ControlChangePayload):
    retries: Optional[int] = Field(None, description="Max retries", alias="retry")
    state: Optional[str] = None
    resource: Optional[KRN] = None
    control_change_id: Optional[UUID] = Field(None, description="Control Change ID")


class RecommendationActions(BaseModel):
    control_changes: List[RecommendationControlChange] = []


class RecommendationPayload(BaseModel):
    source: Optional[KRN] = None
    resource: KRN
    type: str
    description: Optional[str] = None
    confidence: Optional[int] = Field(None, ge=1, le=4)
    expiration_date: Optional[datetime] = None
    actions: RecommendationActions = RecommendationActions()
    metadata: Dict[str, Any] = {}
    state: Optional[Literal["pending", "auto_accepted"]] = None
    evidences: List[BaseEvidence] = []
    custom_identifier: Optional[str] = None


class RecommendationMsg(Message):
    TYPE_ = KMessageTypeRecommendation()

    payload: RecommendationPayload


class EdgeParameter(BaseModel):
    name: str
    value: Union[StrictBool, StrictInt, StrictFloat, StrictStr]
    comment: Optional[str] = None


class ResourceParameters(BaseModel):
    resource: KRN
    parameters: List[EdgeParameter]


class ParametersPayload(BaseModel):
    source: Optional[KRN] = None
    resource_parameters: List[ResourceParameters]


class ParametersMsg(Message):
    TYPE_ = KMessageTypeParameters()

    payload: ParametersPayload


class ManifestDatastream(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    primitive_type_name: Optional[str] = None
    data_type_name: Optional[str] = None
    semantic_type_name: Optional[str] = None
    unit_name: Optional[str] = None


class ResourceDatastream(BaseModel):
    map_to: Optional[str] = None
    remote: Optional[bool] = None
    access: Literal["RO", "RW", "WO"] = "RO"
    owned: Optional[bool] = False
    configuration: Dict = {}


class Resource(BaseModel):
    type: str = ""
    name: str = ""
    properties: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}
    parameters: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}
    datastreams: Dict[str, ResourceDatastream] = {}


class RuntimeManifestPayload(BaseModel):
    resources: List[Resource] = []
    configuration: Dict = {}
    datastreams: List[ManifestDatastream] = []


class RuntimeManifest(Message):
    TYPE_ = KMessageTypeRuntimeManifest()

    payload: RuntimeManifestPayload


class DataTagPayload(BaseModel):
    start_date: datetime
    end_date: datetime
    tag_name: str
    resource: KRNAsset
    description: Optional[str] = Field(None, max_length=256)
    contexts: Optional[List[KRN]] = None
    source: Optional[KRN] = None


class DataTagMsg(Message):
    TYPE_ = KMessageTypeDataTag()

    resource: KRNAsset
    payload: DataTagPayload
