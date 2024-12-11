from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from kelvin.krn import KRN, KRNAppVersion, KRNAsset, KRNAssetDataStream, KRNAssetParameter
from kelvin.message import Message
from kelvin.message.base_messages import (
    ControlChangeAck,
    ControlChangeMsg,
    ControlChangePayload,
    ControlChangeStatusPayload,
    DataTagMsg,
    DataTagPayload,
    EdgeParameter,
    ParametersMsg,
    ParametersPayload,
    RecommendationActions,
    RecommendationControlChange,
    RecommendationMsg,
    RecommendationPayload,
    ReportedValues,
    ResourceParameters,
    StateEnum,
    ValuePoint,
)
from kelvin.message.evidences import BaseEvidence, Evidence


class MessageBuilder(ABC):
    @abstractmethod
    def to_message(self) -> Message:
        pass


@dataclass
class ControlChange(MessageBuilder):
    """Control change builder
    Use this helper class to build a Kelvin Control change.

    Args:
        resource (KRN): The kelvin resource targeted by the control change, represented by a KRN (usually
            KRNAssetDataStream)
        expiration_date (datetime | timedelta): The absolute time in the future when the Control Change expires. Provide
            either a absolute datetime or a timedelta from now
        payload (bool, int, float, str): The desired target value for the control change
        retries (int): Optional number of retries
        timeout (int): Optional timeout time (for retries)
        control_change_id (UUID): Optional UUID to set an specific ID for the control change
        from_value (ValuePoint): Optional initial value for the control change
        trace_id (UUID): Optional trace ID for the control change
    """

    resource: KRN
    expiration_date: Union[datetime, timedelta]
    payload: Any
    retries: Optional[int] = None
    timeout: Optional[int] = None
    control_change_id: Optional[UUID] = None
    from_value: Optional[ValuePoint] = None
    trace_id: Optional[UUID] = None

    def to_message(self) -> ControlChangeMsg:
        if isinstance(self.expiration_date, datetime):
            expiration = self.expiration_date
        else:
            expiration = datetime.now() + self.expiration_date

        return ControlChangeMsg(
            id=self.control_change_id if self.control_change_id is not None else uuid4(),
            trace_id=self.trace_id,
            resource=self.resource,
            payload=ControlChangePayload(
                timeout=self.timeout,
                retries=self.retries,
                expiration_date=expiration,
                payload=self.payload,
                from_value=self.from_value,
            ),
        )


@dataclass
class Recommendation(MessageBuilder):
    """Recommendation Builder. Use this helper class to build a Kelvin Recommendation.

    Args:
        resource (KRNAsset): The kelvin asset resource targeted by the recommendation
        type (str): the type of the recommendation, chose one from the available on the kelvin platform (eg generic,
            speed_inc, speed_dec, ...)
        expiration_date (datetime | timedelta): The absolute time in the future when the recommendation expires. Provide
            either a absolute datetime or a timedelta from now
        description (str): An optional description for the recommendation
        confidence (int): Optional confidence of the recommendation (from 1 to 4)
        control_changes (list[ControlChanges]): the list of ControlChanges associated with the recommendation
        metadata: Dict[str, Any]: Optional metadata for the recommendation
        auto_accepted (bool): Sets the Recommendation as auto accepted. Default is False
    """

    resource: KRNAsset
    type: str
    expiration_date: Optional[Union[datetime, timedelta]] = None
    description: Optional[str] = None
    confidence: Optional[int] = Field(default=None, ge=1, le=4)
    control_changes: List[ControlChange] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    auto_accepted: bool = False
    evidences: List[Evidence] = Field(default_factory=list)
    custom_identifier: Optional[str] = None

    def to_message(self) -> RecommendationMsg:
        ccs = []
        for cc in self.control_changes:
            if isinstance(cc.expiration_date, datetime):
                cc_expiration = cc.expiration_date
            else:
                cc_expiration = datetime.now() + cc.expiration_date
            ccs.append(
                RecommendationControlChange(
                    retry=cc.retries,
                    timeout=cc.timeout,
                    expiration_date=cc_expiration,
                    payload=cc.payload,
                    resource=cc.resource,
                    control_change_id=cc.control_change_id,
                    from_value=cc.from_value,
                )
            )

        if self.expiration_date is None:
            rec_expiration_date = None
        elif isinstance(self.expiration_date, datetime):
            rec_expiration_date = self.expiration_date
        else:
            rec_expiration_date = datetime.now() + self.expiration_date

        return RecommendationMsg(
            resource=self.resource,
            payload=RecommendationPayload(
                resource=self.resource,
                type=self.type,
                description=self.description,
                expiration_date=rec_expiration_date,
                confidence=self.confidence,
                actions=RecommendationActions(control_changes=ccs),
                metadata=self.metadata,
                state="auto_accepted" if self.auto_accepted is True else None,
                evidences=[BaseEvidence(type=ev._TYPE, payload=ev) for ev in self.evidences],
                custom_identifier=self.custom_identifier,
            ),
        )


@dataclass
class AssetParameter:
    """Asset Parameter Helper.

    Args:
        resource (KRNAssetParameter): Kelvin Resource name for the target Asset Parameter
        value (Union[bool, int, float, string]): parameter value
        comment (Optional[str]): optional comment for parameter change
    """

    resource: KRNAssetParameter
    value: Union[StrictBool, StrictInt, StrictFloat, StrictStr]
    comment: Optional[str] = None


@dataclass
class AssetParameters(MessageBuilder):
    """Parameters Builder. Set application parameters in bulk.

    Args:
        resource (Optional[KRNAppVersion]): Optional Kelvin Resource name for the target App Version.
            Defaults to current app.
        parameters (List[AssetParameters]): list of single asset parameters
    """

    parameters: List[AssetParameter]
    resource: Optional[KRNAppVersion] = None

    def to_message(self) -> ParametersMsg:
        asset_params: Dict[str, List[EdgeParameter]] = {}
        for asset_param in self.parameters:
            asset_params.setdefault(asset_param.resource.asset, []).append(
                EdgeParameter(name=asset_param.resource.parameter, value=asset_param.value, comment=asset_param.comment)
            )

        param_models = [
            ResourceParameters(resource=KRNAsset(asset), parameters=params) for asset, params in asset_params.items()
        ]

        return ParametersMsg(resource=self.resource, payload=ParametersPayload(resource_parameters=param_models))


@dataclass
class DataTag(MessageBuilder):
    """Data Tag.

    Args:
       start_date (datetime): The start date of the data tag.
       tag_name (str): The name of the data tag.
       resource (KRNAsset): The asset resource associated with the data tag.
       end_date (Optional[datetime]): The end date of the data tag. If not specified, the data tag is
       considered one point in time, the start_date.
       contexts (Optional[List[KRN]]): The list of contexts associated with the data tag.
       description (Optional[str]): The description of the data tag. Truncated to 256 characters.
    """

    start_date: datetime
    tag_name: str
    resource: KRNAsset
    end_date: Optional[datetime] = None
    contexts: Optional[List[KRN]] = None
    description: Optional[str] = None

    def to_message(self) -> DataTagMsg:
        end_date = self.end_date or self.start_date
        description = self.description[:256] if self.description else None

        return DataTagMsg(
            resource=self.resource,
            payload=DataTagPayload(
                start_date=self.start_date,
                end_date=end_date,
                tag_name=self.tag_name,
                resource=self.resource,
                description=description,
                contexts=self.contexts,
            ),
        )


@dataclass
class ControlAck(MessageBuilder):
    """Control Change Ack

    Args:
        resource (KRNAssetDataStream): The resource associated with the control change
        state (StateEnum): The state of the control change
        message (Optional[str]): Optional message
        before (Optional[ValuePoint]): Optional value point before the control change
        after (Optional[ValuePoint]): Optional value point after the control change
    """

    resource: KRNAssetDataStream
    state: StateEnum
    message: Optional[str] = None
    before: Optional[ValuePoint] = None
    after: Optional[ValuePoint] = None

    def to_message(self) -> ControlChangeAck:
        return ControlChangeAck(
            resource=self.resource,
            payload=ControlChangeStatusPayload(
                state=self.state,
                message=self.message,
                reported=ReportedValues(before=self.before, after=self.after) if self.before or self.after else None,
            ),
        )
