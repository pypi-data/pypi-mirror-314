from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ConfigurationError(Exception):
    pass


class MetricInfo(BaseModel):
    model_config = {"extra": "allow"}

    asset_names: Optional[List[str]] = []


class Metric(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    data_type: str
    control_change: bool = False


class ParameterDefinition(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    data_type: str
    default: Optional[Dict] = None


class MetricInput(Metric):
    model_config = {"extra": "allow"}

    sources: Optional[List[MetricInfo]] = []


class MetricOutput(Metric):
    model_config = {"extra": "allow"}

    targets: Optional[List[MetricInfo]] = []


class AssetsEntry(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    parameters: Dict[str, Any] = {}
    properties: Dict[str, Any] = {}


class KelvinAppConfig(BaseModel):
    model_config = {"extra": "allow"}

    assets: List[AssetsEntry] = []
    inputs: List[Metric] = []
    outputs: List[Metric] = []
    parameters: List[ParameterDefinition] = []
    configuration: Dict = {}


class MetricMap(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    asset_name: str
    data_type: str
    access: str = "RO"
    configuration: Dict = {}


class BridgeAppConfig(BaseModel):
    model_config = {"extra": "allow"}

    metrics_map: List[MetricMap] = []
    configuration: Dict = {}


class KelvinAppType(BaseModel):
    model_config = {"extra": "allow"}

    type: str
    kelvin: KelvinAppConfig = KelvinAppConfig()
    bridge: BridgeAppConfig = BridgeAppConfig()


class AppInfo(BaseModel):
    model_config = {"extra": "allow"}

    name: str
    version: str


class AppConfig(BaseModel):
    model_config = {"extra": "allow"}

    app: KelvinAppType
    info: AppInfo
