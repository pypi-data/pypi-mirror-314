"""
Kelvin API Client.
"""

from __future__ import annotations

from functools import wraps
from types import FunctionType, MethodType
from typing import Any, Generic, List, Mapping, Type, TypeVar

from .base_client import BaseClient
from .data_model import DataModel
from .model import domain, models, responses

MODELS: Mapping[str, Type[DataModel]] = {
    "timeseries_projection": domain.TimeseriesProjection,  # type: ignore
    "app_projection": models.AppProjection,  # type: ignore
    "app_version_resumed_projection": models.AppVersionResumedProjection,  # type: ignore
    "app": responses.App,  # type: ignore
    "app_parameter_values": responses.AppParameterValues,  # type: ignore
    "app_version": responses.AppVersion,  # type: ignore
    "asset": responses.Asset,  # type: ignore
    "asset_insights_item": responses.AssetInsightsItem,  # type: ignore
    "asset_item": responses.AssetItem,  # type: ignore
    "asset_status": responses.AssetStatus,  # type: ignore
    "asset_status_count": responses.AssetStatusCount,  # type: ignore
    "asset_type": responses.AssetType,  # type: ignore
    "audit_logger": responses.AuditLogger,  # type: ignore
    "bridge": responses.Bridge,  # type: ignore
    "bridge_item": responses.BridgeItem,  # type: ignore
    "cluster": responses.Cluster,  # type: ignore
    "cluster_manifest_list": responses.ClusterManifestList,  # type: ignore
    "control_change": responses.ControlChange,  # type: ignore
    "control_change_clustering": responses.ControlChangeClustering,  # type: ignore
    "control_change_get": responses.ControlChangeGet,  # type: ignore
    "data": responses.Data,  # type: ignore
    "data_mappings_response": responses.DataMappingsResponse,  # type: ignore
    "data_stream": responses.DataStream,  # type: ignore
    "data_stream_context": responses.DataStreamContext,  # type: ignore
    "data_type": responses.DataType,  # type: ignore
    "deployment": responses.Deployment,  # type: ignore
    "instance_health_status": responses.InstanceHealthStatus,  # type: ignore
    "instance_setting_item": responses.InstanceSettingItem,  # type: ignore
    "node": responses.Node,  # type: ignore
    "parameter_definition_item": responses.ParameterDefinitionItem,  # type: ignore
    "parameter_get_schema": responses.ParameterGetSchema,  # type: ignore
    "parameter_value_item": responses.ParameterValueItem,  # type: ignore
    "planner_rules_response": responses.PlannerRulesResponse,  # type: ignore
    "primitive_type": responses.PrimitiveType,  # type: ignore
    "properties_values": responses.PropertiesValues,  # type: ignore
    "property": responses.Property,  # type: ignore
    "recommendation": responses.Recommendation,  # type: ignore
    "recommendation_clustering": responses.RecommendationClustering,  # type: ignore
    "recommendation_response_payload": responses.RecommendationResponsePayload,  # type: ignore
    "recommendation_type": responses.RecommendationType,  # type: ignore
    "resource_app_projection": responses.ResourceAppProjection,  # type: ignore
    "secret": responses.Secret,  # type: ignore
    "semantic_type": responses.SemanticType,  # type: ignore
    "service_item": responses.ServiceItem,  # type: ignore
    "thread": responses.Thread,  # type: ignore
    "unit": responses.Unit,  # type: ignore
    "user": responses.User,  # type: ignore
    "user_setting_item": responses.UserSettingItem,  # type: ignore
    "user_with_permissions": responses.UserWithPermissions,  # type: ignore
    "workload": responses.Workload,  # type: ignore
    "workload_logs": responses.WorkloadLogs,  # type: ignore
}


T = TypeVar("T", bound=DataModel)


class DataModelProxy(Generic[T]):
    """Proxy client to data models."""

    def __init__(self, model: Type[T], client: Client) -> None:
        """Initialise resource adaptor."""

        self._model = model
        self._client = client

    def new(self, **kwargs: Any) -> T:
        """New instance."""

        return self._model(self._client, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Map name to method."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            f = getattr(self._model, name)
        except AttributeError:
            return super().__getattribute__(name)

        if isinstance(f, (FunctionType, MethodType)):

            @wraps(f)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return f(*args, **kwargs, _client=self._client)

            return wrapper

        return super().__getattribute__(name)

    def __dir__(self) -> List[str]:
        """List methods for model."""

        return sorted(
            k
            for k in vars(self._model)
            if not k.startswith("_")
            and isinstance(getattr(self._model, k), (FunctionType, MethodType))
        )

    def __str__(self) -> str:
        """Return str(self)."""

        return str(self._model)

    def __repr__(self) -> str:
        """Return repr(self)."""

        return repr(self._model)


class Client(BaseClient):
    """
    Kelvin API Client.

    Parameters
    ----------
    config : :obj:`ClientConfiguration`, optional
        Configuration object
    password : :obj:`str`, optional
        Password for obtaining access token
    totp : :obj:`str`, optional
        Time-based one-time password
    verbose : :obj:`bool`, optional
        Log requests/responses
    use_keychain : :obj:`bool`, optional
        Store credentials securely in system keychain
    store_token : :obj:`bool`, optional
        Store access token
    login : :obj:`bool`, optional
        Login to API
    mirror : :obj:`str`, optional
        Directory to use for caching mirrored responses (created if not existing)
    mirror_mode : :obj:`MirrorMode`, :obj:`str` or :obj:`list`, optional
        Mode of response mirroring:
            - ``dump``: Save responses in mirror cache
            - ``load``: Load responses from mirror cache (if available)
            - ``both``: Both dump and load
            - ``none``: Do not dump or load
    _adapter : :obj:`requests.adapters.BaseAdapter`, optional
        Optional requests adapter instance (e.g. :obj:`requests.adapters.HTTPAdapter`).
        Useful for testing.

    """

    timeseries_projection: Type[domain.TimeseriesProjection]
    app_projection: Type[models.AppProjection]
    app_version_resumed_projection: Type[models.AppVersionResumedProjection]
    app: Type[responses.App]
    app_parameter_values: Type[responses.AppParameterValues]
    app_version: Type[responses.AppVersion]
    asset: Type[responses.Asset]
    asset_insights_item: Type[responses.AssetInsightsItem]
    asset_item: Type[responses.AssetItem]
    asset_status: Type[responses.AssetStatus]
    asset_status_count: Type[responses.AssetStatusCount]
    asset_type: Type[responses.AssetType]
    audit_logger: Type[responses.AuditLogger]
    bridge: Type[responses.Bridge]
    bridge_item: Type[responses.BridgeItem]
    cluster: Type[responses.Cluster]
    cluster_manifest_list: Type[responses.ClusterManifestList]
    control_change: Type[responses.ControlChange]
    control_change_clustering: Type[responses.ControlChangeClustering]
    control_change_get: Type[responses.ControlChangeGet]
    data: Type[responses.Data]
    data_mappings_response: Type[responses.DataMappingsResponse]
    data_stream: Type[responses.DataStream]
    data_stream_context: Type[responses.DataStreamContext]
    data_type: Type[responses.DataType]
    deployment: Type[responses.Deployment]
    instance_health_status: Type[responses.InstanceHealthStatus]
    instance_setting_item: Type[responses.InstanceSettingItem]
    node: Type[responses.Node]
    parameter_definition_item: Type[responses.ParameterDefinitionItem]
    parameter_get_schema: Type[responses.ParameterGetSchema]
    parameter_value_item: Type[responses.ParameterValueItem]
    planner_rules_response: Type[responses.PlannerRulesResponse]
    primitive_type: Type[responses.PrimitiveType]
    properties_values: Type[responses.PropertiesValues]
    property: Type[responses.Property]
    recommendation: Type[responses.Recommendation]
    recommendation_clustering: Type[responses.RecommendationClustering]
    recommendation_response_payload: Type[responses.RecommendationResponsePayload]
    recommendation_type: Type[responses.RecommendationType]
    resource_app_projection: Type[responses.ResourceAppProjection]
    secret: Type[responses.Secret]
    semantic_type: Type[responses.SemanticType]
    service_item: Type[responses.ServiceItem]
    thread: Type[responses.Thread]
    unit: Type[responses.Unit]
    user: Type[responses.User]
    user_setting_item: Type[responses.UserSettingItem]
    user_with_permissions: Type[responses.UserWithPermissions]
    workload: Type[responses.Workload]
    workload_logs: Type[responses.WorkloadLogs]

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *MODELS]

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_") or name in super().__dir__():
            return super().__getattribute__(name)  # pragma: no cover

        try:
            model = MODELS[name]
        except KeyError:
            return super().__getattribute__(name)

        return DataModelProxy(model, self)
