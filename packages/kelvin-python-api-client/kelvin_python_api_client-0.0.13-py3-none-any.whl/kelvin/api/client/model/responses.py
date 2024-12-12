from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic.v1 import EmailStr, Field, StrictBool, StrictFloat, StrictInt, StrictStr, constr

from kelvin.api.client.base_model import BaseModelRoot
from kelvin.api.client.data_model import DataModelBase, PaginatorDataModel
from kelvin.krn import KRN, KRNAsset, KRNAssetDataStream

from . import enum, pagination, type
from .type import (
    App,
    AppManagerApp,
    AppManagerAppPlannerRules,
    AppManagerAppVersionSummary,
    AppVersion,
    Asset,
    AssetStatus,
    AssetType,
    Bridge,
    DataStreamDataType,
    DataStreamSemanticType,
    DataTag,
    FileStorage,
    Guardrail,
    InstanceAuditLogItem,
    InstanceSettings,
    InstanceSettingsAppManagerPlannerRules,
    OrchestrationCluster,
    ParameterSchedule,
    Property,
    Recommendation,
    RecommendationActionStatus,
    RecommendationType,
    Tag,
    Thread,
    TimeseriesData,
    Unit,
    UserSetting,
    Workload,
)


class AppManagerAppPlannerRulesGet(AppManagerAppPlannerRules):
    """
    AppManagerAppPlannerRulesGet object.

    Parameters
    ----------

    """


class AppManagerAppPlannerRulesUpdate(AppManagerAppPlannerRules):
    """
    AppManagerAppPlannerRulesUpdate object.

    Parameters
    ----------

    """


class AppManagerAppGet(AppManagerApp):
    """
    AppManagerAppGet object.

    Parameters
    ----------

    """


class AppManagerResourceApp(DataModelBase):
    """
    AppManagerResourceApp object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    version: Optional[StrictStr]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Application.", example="motor-speed-control"
    )
    version: Optional[StrictStr] = Field(
        None, description="Version number of the Application associated with this Asset.", example="1.0.8"
    )


class AppManagerResource(DataModelBase):
    """
    AppManagerResource object.

    Parameters
    ----------
    created: Optional[datetime]
    name: Optional[StrictStr]
    title: Optional[StrictStr]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    name: Optional[StrictStr] = Field(None, description="Unique identifier key `name` of the Asset.", example="well_01")
    title: Optional[StrictStr] = Field(None, description="Display name (`title`) of the Asset.", example="Well 01")
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Asset keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class AppManagerResourceAppStatus(DataModelBase):
    """
    AppManagerResourceAppStatus object.

    Parameters
    ----------
    last_seen: Optional[datetime]
    status: Optional[enum.AppManagerAppStatus]
    updated: Optional[datetime]
    updated_by: Optional[KRN]

    """

    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when this the Application for this Asset was last seen online, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    status: Optional[enum.AppManagerAppStatus] = None
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any of the Asset keys for the Application were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    updated_by: Optional[KRN] = Field(
        None,
        description="User that made the last change to any keys for this Application. Sources are written in the krn format.",
        example="krn:user:person@example.com",
    )


class AppManagerResourceAppWorkload(DataModelBase):
    """
    AppManagerResourceAppWorkload object.

    Parameters
    ----------
    cluster: Optional[constr(max_length=64, strict=True)]
    name: Optional[constr(max_length=32, strict=True)]
    warnings: Optional[List[StrictStr]]

    """

    cluster: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` for the cluster where the Workload is deployed and running.",
        example="cluster_north_01",
    )
    name: Optional[constr(max_length=32, strict=True)] = Field(
        None,
        description="Unique identifier `name` for the Workload that is running the Application for the Asset.",
        example="motor-speed-control-cwgzmh08k21w",
    )
    warnings: Optional[List[StrictStr]] = Field(
        None, description="Any warning messages received from Kubernetes.", example="Exit Code 1."
    )


class AppManagerResourceContext(DataModelBase):
    """
    AppManagerResourceContext object.

    Parameters
    ----------
    app: Optional[AppManagerResourceApp]
    enabled: Optional[StrictBool]
    resource: Optional[AppManagerResource]
    status: Optional[AppManagerResourceAppStatus]
    workload: Optional[AppManagerResourceAppWorkload]

    """

    app: Optional[AppManagerResourceApp] = None
    enabled: Optional[StrictBool] = Field(
        None,
        description="Enabled status of the Application for this Asset. True means that it can run but other factors may cause the Application to fail to run. Check `status` for actual current status.",
        example=True,
    )
    resource: Optional[AppManagerResource] = None
    status: Optional[AppManagerResourceAppStatus] = None
    workload: Optional[AppManagerResourceAppWorkload] = None


class AppManagerAppResourcesListPaginatedResponseCursor(PaginatorDataModel[AppManagerResourceContext]):
    """
    AppManagerAppResourcesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[AppManagerResourceContext]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[AppManagerResourceContext]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Assets associated with the Applications and its associated Workload and status, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AppManagerAppResourcesListPaginatedResponseLimits(PaginatorDataModel[AppManagerResourceContext]):
    """
    AppManagerAppResourcesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[AppManagerResourceContext]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[AppManagerResourceContext]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Assets associated with Applications and its associated Workload and status for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AppManagerAppResourcesListPaginatedResponseStream(AppManagerResourceContext):
    """
    AppManagerAppResourcesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AppIO(DataModelBase):
    """
    AppIO object.

    Parameters
    ----------
    control_change: Optional[StrictBool]
    data_type_name: Optional[constr(max_length=64, strict=True)]
    name: Optional[constr(max_length=64, strict=True)]
    primitive_type_name: Optional[enum.DataType]
    semantic_type_name: Optional[StrictStr]
    unit_name: Optional[StrictStr]

    """

    control_change: Optional[StrictBool] = Field(
        None, description="Variable is tagged as a control change variable.", example=False
    )
    data_type_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Data Type that describes the format of the variable. Only required if the Primitive Type is `object`. Can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="kelvin.pumpcard",
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the Data Stream.", example="gas_flow_rate"
    )
    primitive_type_name: Optional[enum.DataType] = Field(None, description="Primitive data type of the Sematic Type.")
    semantic_type_name: Optional[StrictStr] = Field(
        None,
        description="Unique identifier `name` of the Semantic Type that describes the nature, purpose or origin of the variable.",
        example="volume_flow_rate",
    )
    unit_name: Optional[StrictStr] = Field(
        None,
        description="Unique identifier `name` of the Units that describes the type or category of variable represented by each unit. Only available if the Primitive Type is `number`.",
        example="litre_per_second",
    )


class DSContext(DataModelBase):
    """
    DSContext object.

    Parameters
    ----------
    resource: Optional[KRNAssetDataStream]
    writable: Optional[StrictBool]

    """

    resource: Optional[KRNAssetDataStream] = Field(
        None,
        description="KRN of the Asset which is paired with the Data Stream to make an Asset / Data Stream pair.",
        example="krn:ad:asset/data_stream",
    )
    writable: Optional[StrictBool] = Field(
        None, description="Can write to the Asset / Data Stream pair.", example=False
    )


class IODataStreamContext(DataModelBase):
    """
    IODataStreamContext object.

    Parameters
    ----------
    context: Optional[List[DSContext]]
    datastream_name: Optional[constr(max_length=64, strict=True)]

    """

    context: Optional[List[DSContext]] = Field(
        None,
        description="Array of Asset KRN resources linked to this Data Stream to make multiple Asset / Data Stream pairs.",
    )
    datastream_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Data Stream. This is part of the Asset / Data Stream pair. Assets are listed in the `context` key.",
        example="gas_flow_rate",
    )


class DataMappingIO(DataModelBase):
    """
    DataMappingIO object.

    Parameters
    ----------
    app: Optional[List[AppIO]]
    datastream_context: Optional[List[IODataStreamContext]]

    """

    app: Optional[List[AppIO]] = Field(None, description="Array of variables in the Application.")
    datastream_context: Optional[List[IODataStreamContext]] = Field(
        None, description="Array of Assets paired to each Data Stream."
    )


class AppManagerAppVersionDataMappingGet(DataModelBase):
    """
    AppManagerAppVersionDataMappingGet object.

    Parameters
    ----------
    inputs: Optional[DataMappingIO]
    mappings: Optional[Dict[str, Any]]
    outputs: Optional[DataMappingIO]

    """

    inputs: Optional[DataMappingIO] = Field(
        None, description="Data mapping inputs between Application variables and Asset / Data Stream pairs."
    )
    mappings: Optional[Dict[str, Any]] = Field(None, description="Reserved for future enhancements.")
    outputs: Optional[DataMappingIO] = Field(
        None, description="Data mapping outputs between Application variables and Asset / Data Stream pairs."
    )


class AppManagerAppVersionDeploy(DataModelBase):
    """
    AppManagerAppVersionDeploy object.

    Parameters
    ----------
    actions: Optional[List[Dict[str, Any]]]
    success: Optional[StrictBool]

    """

    actions: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Additional information on the results of the deploy actions, including type of action, resources added and Workload `name` created. See example.",
    )
    success: Optional[StrictBool] = Field(None, description="Whether the deploy was successful.", example=True)


class AppManagerAppVersionQuickdeploy(AppManagerAppVersionDeploy):
    """
    AppManagerAppVersionQuickdeploy object.

    Parameters
    ----------

    """


class AppManagerListPaginatedResponseCursor(PaginatorDataModel[type.AppManagerApp]):
    """
    AppManagerListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.AppManagerApp]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.AppManagerApp]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Applications and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AppManagerListPaginatedResponseLimits(PaginatorDataModel[type.AppManagerApp]):
    """
    AppManagerListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.AppManagerApp]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.AppManagerApp]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Applications and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AppManagerListPaginatedResponseStream(AppManagerApp):
    """
    AppManagerListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AppManagerResourceGetPaginatedResponseCursor(PaginatorDataModel[type.AppManagerAppVersionSummary]):
    """
    AppManagerResourceGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.AppManagerAppVersionSummary]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.AppManagerAppVersionSummary]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Application objects associated with the Asset (`resource`). More detailed information on the Applications can be retrieved from the App Manager Get Application API.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AppManagerResourceGetPaginatedResponseLimits(PaginatorDataModel[type.AppManagerAppVersionSummary]):
    """
    AppManagerResourceGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.AppManagerAppVersionSummary]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.AppManagerAppVersionSummary]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Application objects associated with the Asset (`resource`). More detailed information on the Applications can be retrieved from the App Manager Get Application API.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AppManagerResourceGetPaginatedResponseStream(AppManagerAppVersionSummary):
    """
    AppManagerResourceGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class AppCreate(App):
    """
    AppCreate object.

    Parameters
    ----------

    """


class Type(Enum):
    system = "system"


class ErrorMessage(DataModelBase):
    """
    ErrorMessage object.

    Parameters
    ----------
    error_code: Optional[StrictInt]
    http_status_code: Optional[StrictInt]
    message: Optional[List[StrictStr]]
    type: Optional[Type]

    """

    error_code: Optional[StrictInt] = Field(
        None, description="Internal Kelvin error code (used for internal purposes).", example=32
    )
    http_status_code: Optional[StrictInt] = Field(None, description="HTTP status error code.", example="4XX")
    message: Optional[List[StrictStr]] = Field(
        None, description="Detailed description of the error.", example=["Detailed information about the error."]
    )
    type: Optional[Type] = Field(None, description="The type of error that has occured, e.g. `system`.")


class AppItem(DataModelBase):
    """
    AppItem object.

    Parameters
    ----------
    created: Optional[datetime]
    description: Optional[constr(max_length=256, strict=True)]
    latest_version: Optional[StrictStr]
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]
    type: Optional[enum.AppType]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the App was first uploaded to the App Registry, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None,
        description="Description of the App in the App Registry.",
        example="""This application controls the speed of the beam pump motor in order to increase production for this type of artificial lift well. It uses values available from the control system such as Downhole Pressure, Motor Speed, Motor Torque and Choke position.
""",
    )
    latest_version: Optional[StrictStr] = Field(
        None, description="Latest version number of the App in the App Registry.", example="1.2.0"
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the App in the App Registry.", example="motor-speed-control"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the App in the App Registry.", example="Motor Speed Control"
    )
    type: Optional[enum.AppType] = Field(
        None,
        description="Type of development used for the App. `kelvin` is Kelvin App using Python and `docker` is using the generic Dockerfile format.",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any App keys in the App Registry were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )


class AppRegistryAppsListPaginatedResponseCursor(PaginatorDataModel[AppItem]):
    """
    AppRegistryAppsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[AppItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[AppItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Type objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AppRegistryAppsListPaginatedResponseLimits(PaginatorDataModel[AppItem]):
    """
    AppRegistryAppsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[AppItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[AppItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Type objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AppRegistryAppsListPaginatedResponseStream(AppItem):
    """
    AppRegistryAppsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AppRegistryAppGet(App):
    """
    AppRegistryAppGet object.

    Parameters
    ----------

    """


class AppUpdate(App):
    """
    AppUpdate object.

    Parameters
    ----------

    """


class AppVersionGet(AppVersion):
    """
    AppVersionGet object.

    Parameters
    ----------

    """


class State(Enum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class AssetInsightsItem(DataModelBase):
    """
    AssetInsightsItem object.

    Parameters
    ----------
    asset_type_name: Optional[StrictStr]
    asset_type_title: Optional[constr(max_length=64, strict=True)]
    extra_fields: Optional[Dict[str, Any]]
    last_seen: Optional[datetime]
    name: Optional[constr(max_length=64, strict=True)]
    pinned: Optional[StrictBool]
    state: Optional[State]
    title: Optional[constr(max_length=64, strict=True)]

    """

    asset_type_name: Optional[StrictStr] = Field(
        None, description="Unique identifier `name` of the Asset Type linked to this Asset.", example="beam_pump"
    )
    asset_type_title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the Asset Type.", example="Well 01"
    )
    extra_fields: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary of all requested data from the `extra_fields` key in the request body. The key names and values for each column of data are defined in the request body.",
    )
    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when this the Asset was last seen online, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the Asset.", example="well_01"
    )
    pinned: Optional[StrictBool] = Field(
        None,
        description="Pinned status of the Asset. The pinned Assets are defined in an array from the request in the key `PinnedAssets`.",
        example=True,
    )
    state: Optional[State] = Field(None, description="Current status (`state`) of the Asset.", example="offline")
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the Asset.", example="Well 01"
    )


class AssetInsightsGetPaginated(PaginatorDataModel[AssetInsightsItem]):
    """
    AssetInsightsGetPaginated object.

    Parameters
    ----------
    data: Optional[List[AssetInsightsItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[AssetInsightsItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Asset objects starting from `page` number.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AssetCreate(Asset):
    """
    AssetCreate object.

    Parameters
    ----------

    """


class AssetsListPaginatedResponseCursor(PaginatorDataModel[type.Asset]):
    """
    AssetsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Asset]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Asset]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Assets objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AssetsListPaginatedResponseLimits(PaginatorDataModel[type.Asset]):
    """
    AssetsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Asset]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Asset]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Assets objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AssetsListPaginatedResponseStream(Asset):
    """
    AssetsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AssetsAdvancedListPaginatedResponseCursor(AssetsListPaginatedResponseCursor):
    """
    AssetsAdvancedListPaginatedResponseCursor object.

    Parameters
    ----------

    """


class AssetsAdvancedListPaginatedResponseLimits(AssetsListPaginatedResponseLimits):
    """
    AssetsAdvancedListPaginatedResponseLimits object.

    Parameters
    ----------

    """


class AssetsAdvancedListPaginatedResponseStream(AssetsListPaginatedResponseStream):
    """
    AssetsAdvancedListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AssetPropertyDefinitionsListPaginatedResponseCursor(PaginatorDataModel[type.Property]):
    """
    AssetPropertyDefinitionsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Property]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Property]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Asset Property objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AssetPropertyDefinitionsListPaginatedResponseLimits(PaginatorDataModel[type.Property]):
    """
    AssetPropertyDefinitionsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Property]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Property]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Asset Property objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AssetPropertyDefinitionsListPaginatedResponseStream(Property):
    """
    AssetPropertyDefinitionsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AssetPropertyValuesGet(DataModelBase):
    """
    AssetPropertyValuesGet object.

    Parameters
    ----------
    properties: Optional[Dict[str, List[Union[StrictInt, StrictFloat, StrictStr, StrictBool]]]]

    """

    properties: Optional[Dict[str, List[Union[StrictInt, StrictFloat, StrictStr, StrictBool]]]] = Field(
        None,
        description="Dictionary containing the `name` of the Asset Property and an array of the associated values.",
        example={"area": ["North", "South", "Central", "Easy", "West"], "fluid-level-high": [200]},
    )


class AssetStatusCountGet(DataModelBase):
    """
    AssetStatusCountGet object.

    Parameters
    ----------
    offline: Optional[StrictInt]
    online: Optional[StrictInt]
    total: Optional[StrictInt]
    unknown: Optional[StrictInt]

    """

    offline: Optional[StrictInt] = Field(
        None, description="Count of all Assets that are inactive and not receiving data.", example=592
    )
    online: Optional[StrictInt] = Field(
        None, description="Count of all Assets that are receiving active data.", example=2787
    )
    total: Optional[StrictInt] = Field(None, description="Count of all Assets.", example=3429)
    unknown: Optional[StrictInt] = Field(
        None,
        description="Count of all Assets that has no Data Streams or all Data Streams have never received data.",
        example=50,
    )


class AssetStatusCurrentGet(AssetStatus):
    """
    AssetStatusCurrentGet object.

    Parameters
    ----------

    """


class AssetTypeCreate(AssetType):
    """
    AssetTypeCreate object.

    Parameters
    ----------

    """


class AssetTypesListPaginatedResponseCursor(PaginatorDataModel[type.AssetType]):
    """
    AssetTypesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.AssetType]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.AssetType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Asset Types objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class AssetTypesListPaginatedResponseLimits(PaginatorDataModel[type.AssetType]):
    """
    AssetTypesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.AssetType]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.AssetType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Asset Types objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class AssetTypesListPaginatedResponseStream(AssetType):
    """
    AssetTypesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AssetTypesAdvancedListPaginatedResponseCursor(AssetTypesListPaginatedResponseCursor):
    """
    AssetTypesAdvancedListPaginatedResponseCursor object.

    Parameters
    ----------

    """


class AssetTypesAdvancedListPaginatedResponseLimits(AssetTypesListPaginatedResponseLimits):
    """
    AssetTypesAdvancedListPaginatedResponseLimits object.

    Parameters
    ----------

    """


class AssetTypesAdvancedListPaginatedResponseStream(AssetTypesListPaginatedResponseStream):
    """
    AssetTypesAdvancedListPaginatedResponseStream object.

    Parameters
    ----------

    """


class AssetTypeGet(AssetType):
    """
    AssetTypeGet object.

    Parameters
    ----------

    """


class AssetTypeUpdate(AssetType):
    """
    AssetTypeUpdate object.

    Parameters
    ----------

    """


class AssetGet(Asset):
    """
    AssetGet object.

    Parameters
    ----------

    """


class AssetUpdate(Asset):
    """
    AssetUpdate object.

    Parameters
    ----------

    """


class BridgeDeploy(Bridge):
    """
    BridgeDeploy object.

    Parameters
    ----------

    """


class BridgeItem(DataModelBase):
    """
    BridgeItem object.

    Parameters
    ----------
    cluster_name: Optional[constr(max_length=64, strict=True)]
    created: Optional[datetime]
    enabled: Optional[StrictBool]
    name: Optional[constr(max_length=32, strict=True)]
    node_name: Optional[constr(max_length=64, strict=True)]
    status: Optional[type.WorkloadStatus]
    title: Optional[StrictStr]
    updated: Optional[datetime]
    workload_name: Optional[constr(max_length=32, strict=True)]
    app_name: Optional[constr(max_length=64, strict=True)]
    app_version: Optional[StrictStr]

    """

    cluster_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Bridge (Connection) was first created, formatted in RFC 3339.",
        example="2023-12-26T18:22:18.582724Z",
    )
    enabled: Optional[StrictBool] = Field(
        None,
        description="If true, Bridge (Connection) `status` is set to `running` and will process I/O's. If false, Bridge (Connection) `status` is set to `stopped` but remains in Node on the Edge System.",
        example=True,
    )
    name: Optional[constr(max_length=32, strict=True)] = Field(
        None, description="Unique identifier `name` of the Bridge (Connection).", example="motor-plc-opcua-connection"
    )
    node_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Node in the Cluster hosting the Bridge (Connection).",
        example="docs-demo-node-01",
    )
    status: Optional[type.WorkloadStatus] = None
    title: Optional[StrictStr] = Field(
        None, description="Display name (`title`) of the Bridge (Connection).", example="Motor PLC OPCUA Connection"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Bridge (Connection) keys were last updated, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    workload_name: Optional[constr(max_length=32, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Workload that the Bridge (Connection) App is deployed as to the Cluster.",
        example="motor-plc-opcua-connection",
    )
    app_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the App. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="test-app",
    )
    app_version: Optional[StrictStr] = Field(None, description="App version", example="1.2.0")


class BridgesListPaginatedResponseCursor(PaginatorDataModel[BridgeItem]):
    """
    BridgesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[BridgeItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[BridgeItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Bridge (Connection) objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class BridgesListPaginatedResponseLimits(PaginatorDataModel[BridgeItem]):
    """
    BridgesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[BridgeItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[BridgeItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Bridge (Connection) objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class BridgesListPaginatedResponseStream(BridgeItem):
    """
    BridgesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class BridgeGet(Bridge):
    """
    BridgeGet object.

    Parameters
    ----------

    """


class ControlChangeClustering(DataModelBase):
    """
    ControlChangeClustering object.

    Parameters
    ----------
    control_change_ids: Optional[List[UUID]]
    count: Optional[StrictInt]
    time_bucket_start: Optional[datetime]

    """

    control_change_ids: Optional[List[UUID]] = Field(
        None,
        description="An array of Control Change `id`'s that have been counted.",
        example=["0002bc79-b42f-461b-95d6-cf0a28ba87aa", "518bcb79-ffaa-4d3f-8042-52634c34b71e"],
    )
    count: Optional[StrictInt] = Field(
        None,
        description="Number of occurrences of Control Changes over the time period of `time_bucket` that meet the request parameters starting from time `time_bucket_start`.",
        example=2,
    )
    time_bucket_start: Optional[datetime] = Field(
        None,
        description="Time of the start of the count for the current `time_bucket` period in RFC 3339 UTC date/time format.",
        example="2023-11-18T18:22:18.582724Z",
    )


class ControlChangeCreate(DataModelBase):
    """
    ControlChangeCreate object.

    Parameters
    ----------
    created_by: Optional[constr(max_length=256, strict=True)]
    created_type: Optional[StrictStr]
    id: UUID
    last_state: Optional[enum.ControlChangeState]
    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    resource: Optional[KRNAssetDataStream]
    source: Optional[KRN]
    timestamp: Optional[datetime]
    trace_id: UUID

    """

    created_by: Optional[constr(max_length=256, strict=True)] = Field(
        None,
        description="Name of the process that created the Control Change. This could be a user, workload, application, etc.",
        example=["krn:user:person@kelvin.ai", "krn:app:motor_speed_control"],
    )
    created_type: Optional[StrictStr] = Field(
        None,
        description="Type of process that created the Control Change. This is inferred from `source`.",
        example="recommendation",
    )
    id: UUID = Field(
        ...,
        description="A unique random generated UUID as the key `id` for the Control Change.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    last_state: Optional[enum.ControlChangeState] = Field(None, description="Current state of the Control Change.")
    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None,
        description="The new value payload to be applied to the Asset / Data Stream pair in `resource`.",
        example=2000,
    )
    resource: Optional[KRNAssetDataStream] = Field(
        None,
        description="The asset / data stream pair that this Control Change will be applied to.",
        example="krn:ad:beam_pump_01/motor_speed_set_point",
    )
    source: Optional[KRN] = Field(
        None,
        description="The process that created the Control Change request. This can be a user or an automated process like a workload, application, recommendation, etc.",
        example="krn:ad:beam_pump_01/motor_speed_set_point",
    )
    timestamp: Optional[datetime] = Field(
        None,
        description="UTC time when the log was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    trace_id: UUID = Field(
        ...,
        description="This is for internal purposes and is the same as the `id`.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )


class ControlChangeGetStatus(DataModelBase):
    """
    ControlChangeGetStatus object.

    Parameters
    ----------
    message: Optional[StrictStr]
    reported: Optional[type.ControlChangeReported]
    state: enum.ControlChangeState
    timestamp: Optional[datetime]

    """

    message: Optional[StrictStr] = Field(
        None, description="A message about the change in status. This will only appear if there is a message attached."
    )
    reported: Optional[type.ControlChangeReported] = None
    state: enum.ControlChangeState = Field(..., description="Control Change state when log was created.")
    timestamp: Optional[datetime] = Field(
        None,
        description="UTC time when the log was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class ControlChangeGet(DataModelBase):
    """
    ControlChangeGet object.

    Parameters
    ----------
    created: Optional[datetime]
    created_by: Optional[constr(max_length=256, strict=True)]
    created_type: Optional[StrictStr]
    id: UUID
    last_message: Optional[StrictStr]
    last_state: Optional[enum.ControlChangeState]
    retries: Optional[StrictInt]
    timeout: Optional[StrictInt]
    expiration_date: Optional[datetime]
    from_: Optional[type.ControlChangeFrom]
    reported: Optional[type.ControlChangeReported]
    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    resource: KRNAssetDataStream
    status_log: Optional[List[ControlChangeGetStatus]]
    timestamp: Optional[datetime]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Control Change was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    created_by: Optional[constr(max_length=256, strict=True)] = Field(
        None,
        description="Name of the process that created the Control Change. This could be a user, workload, application, recommendation, etc.",
        example=["krn:user:person@kelvin.ai", "krn:app:motor_speed_control"],
    )
    created_type: Optional[StrictStr] = Field(
        None,
        description="Type of process that created the Control Change. This is inferred from `source`.",
        example="recommendation",
    )
    id: UUID = Field(
        ...,
        description="A unique random generated UUID as the key `id` for the Control Change.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    last_message: Optional[StrictStr] = Field(
        None,
        description="Last message received from the Control Change Manager.",
        example="The Control Change was sent to the Bridge. At this stage, the system is monitoring according to the Acceptance Criteria parameters and the retry logic.",
    )
    last_state: Optional[enum.ControlChangeState] = Field(None, description="Current state of the Control Change.")
    retries: Optional[StrictInt] = Field(
        None,
        description="How many times the Control Change Manager will try and send the same Control Change request to the Bridge before the change is tagged `failed` and no further attempts will be made. If the Bridge sends a `processed` acknowledgment, then the Control Change Manager will stop any further retries and wait for an `applied` response.",
        example=3,
    )
    timeout: Optional[StrictInt] = Field(
        None,
        description="How long the Control Change Manager will wait in seconds for the Bridge to send a `processed` acknowledgement before a retry will be attempted. If the total number of retries has reach its `retries` limit, then the change is tagged `failed` and no further attempts will be made.",
        example=150,
    )
    expiration_date: Optional[datetime] = Field(
        None,
        description="UTC time when the Control Change will expire and the `status` automatically marked as `failed`, formatted in RFC 3339..",
    )
    from_: Optional[type.ControlChangeFrom] = Field(None, alias="from")
    reported: Optional[type.ControlChangeReported] = None
    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None,
        description="The new value payload to be applied to the Asset / Data Stream pair in `resource`.",
        example=2000,
    )
    resource: KRNAssetDataStream = Field(
        ...,
        description="The asset / data stream pair that this Control Change will be applied to.",
        example="krn:ad:beam_pump_01/motor_speed_set_point",
    )
    status_log: Optional[List[ControlChangeGetStatus]] = Field(
        None, description="Array of dictionary objects with the details of each `status` change."
    )
    timestamp: Optional[datetime] = Field(
        None,
        description="UTC time when the Control Change was created, formatted in RFC 3339.",
        example="2023-11-13T12:00:00Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Control Change keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class ControlChangeLastGetPaginatedResponseCursor(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangeLastGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ControlChangeLastGetPaginatedResponseLimits(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangeLastGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ControlChangeLastGetPaginatedResponseStream(ControlChangeGet):
    """
    ControlChangeLastGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class ControlChangesListPaginatedResponseCursor(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ControlChangesListPaginatedResponseLimits(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ControlChangesListPaginatedResponseStream(ControlChangeGet):
    """
    ControlChangesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class ControlChangeRangeGetPaginatedResponseCursor(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangeRangeGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ControlChangeRangeGetPaginatedResponseLimits(PaginatorDataModel[ControlChangeGet]):
    """
    ControlChangeRangeGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ControlChangeGet]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ControlChangeGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Control Changes and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ControlChangeRangeGetPaginatedResponseStream(ControlChangeGet):
    """
    ControlChangeRangeGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class DataStreamsDataTypesListPaginatedResponseCursor(PaginatorDataModel[type.DataStreamDataType]):
    """
    DataStreamsDataTypesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.DataStreamDataType]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.DataStreamDataType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Type objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataStreamsDataTypesListPaginatedResponseLimits(PaginatorDataModel[type.DataStreamDataType]):
    """
    DataStreamsDataTypesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.DataStreamDataType]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.DataStreamDataType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Type objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataStreamsDataTypesListPaginatedResponseStream(DataStreamDataType):
    """
    DataStreamsDataTypesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class DataStreamSemanticTypeCreate(DataStreamSemanticType):
    """
    DataStreamSemanticTypeCreate object.

    Parameters
    ----------

    """


class DataStreamSemanticTypeUpdate(DataStreamSemanticType):
    """
    DataStreamSemanticTypeUpdate object.

    Parameters
    ----------

    """


class DataStreamSemanticTypeGet(DataStreamSemanticType):
    """
    DataStreamSemanticTypeGet object.

    Parameters
    ----------

    """


class DataStreamsSemanticTypesListPaginatedResponseCursor(PaginatorDataModel[type.DataStreamSemanticType]):
    """
    DataStreamsSemanticTypesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.DataStreamSemanticType]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.DataStreamSemanticType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Semantic Type objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataStreamsSemanticTypesListPaginatedResponseLimits(PaginatorDataModel[type.DataStreamSemanticType]):
    """
    DataStreamsSemanticTypesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.DataStreamSemanticType]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.DataStreamSemanticType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Semantic Type objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataStreamsSemanticTypesListPaginatedResponseStream(DataStreamSemanticType):
    """
    DataStreamsSemanticTypesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class DataStreamUnitCreate(Unit):
    """
    DataStreamUnitCreate object.

    Parameters
    ----------

    """


class DataStreamUnitUpdate(Unit):
    """
    DataStreamUnitUpdate object.

    Parameters
    ----------

    """


class DataStreamUnitGet(Unit):
    """
    DataStreamUnitGet object.

    Parameters
    ----------

    """


class DataStreamsUnitsListPaginatedResponseCursor(PaginatorDataModel[type.Unit]):
    """
    DataStreamsUnitsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Unit]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Unit]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Unit objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataStreamsUnitsListPaginatedResponseLimits(PaginatorDataModel[type.Unit]):
    """
    DataStreamsUnitsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Unit]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Unit]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Unit objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataStreamsUnitsListPaginatedResponseStream(Unit):
    """
    DataStreamsUnitsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class TypeModel(Enum):
    computed = "computed"
    measurement = "measurement"


class DataStream(DataModelBase):
    """
    DataStream object.

    Parameters
    ----------
    created: Optional[datetime]
    description: Optional[constr(max_length=200, strict=True)]
    name: Optional[StrictStr]
    data_type_name: Optional[enum.DataType]
    semantic_type_name: Optional[StrictStr]
    title: Optional[constr(max_length=64, strict=True)]
    type: Optional[TypeModel]
    unit_name: Optional[StrictStr]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Data Stream was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    description: Optional[constr(max_length=200, strict=True)] = Field(
        None,
        description="Detailed description of the Data Stream.",
        example="The rate at which gas flows from the reservoir to the surface.",
    )
    name: Optional[StrictStr] = Field(
        None, description="Unique identifier `name` of the Data Stream.", example="gas_flow_rate"
    )
    data_type_name: Optional[enum.DataType] = Field(None, description="Data type of the Data Stream.")
    semantic_type_name: Optional[StrictStr] = Field(
        None,
        description="Unique identifier `name` of the Semantic Type that describes the nature, purpose or origin of the data.",
        example="volume_flow_rate",
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the Data Stream.", example="Gas Flow Rate"
    )
    type: Optional[TypeModel] = Field(
        None, description="Specifies the technique used for generating data in the Data Stream.", example="measurement"
    )
    unit_name: Optional[StrictStr] = Field(
        None,
        description="Unique identifier `name` of the Units that describes the type or category of data represented by each unit. Only available if the Primitive Type is `number`.",
        example="litre_per_second",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Data Stream keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class DataStreamCreate(DataStream):
    """
    DataStreamCreate object.

    Parameters
    ----------

    """


class DataStreamUpdate(DataStream):
    """
    DataStreamUpdate object.

    Parameters
    ----------

    """


class DataStreamGet(DataStream):
    """
    DataStreamGet object.

    Parameters
    ----------

    """


class DataStreamsListPaginatedResponseCursor(PaginatorDataModel[DataStream]):
    """
    DataStreamsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[DataStream]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[DataStream]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Streams objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataStreamsListPaginatedResponseLimits(PaginatorDataModel[DataStream]):
    """
    DataStreamsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[DataStream]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[DataStream]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Streams objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataStreamsListPaginatedResponseStream(DataStream):
    """
    DataStreamsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class Context(DataModelBase):
    """
    Context object.

    Parameters
    ----------
    created: Optional[datetime]
    resource: Optional[KRNAsset]
    source: Optional[KRN]
    updated: Optional[datetime]
    writable: Optional[StrictBool]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Asset / Data Stream pair was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    resource: Optional[KRNAsset] = Field(
        None, description="Asset `name` that is associated with the Data Stream.", example="krn:asset:bp_16"
    )
    source: Optional[KRN] = Field(
        None,
        description="Workload `name` that is sending data to the Asset / Data Stream pair.",
        example="krn:wlappv:cluster1/app1/1.2.0",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Asset / Data Stream pair keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    writable: Optional[StrictBool] = Field(
        None,
        description="Indicates whether the Asset / Data Stream pair `write` key is read/write (`true`) or read only (`false`).",
        example=True,
    )


class DataStreamContext(DataModelBase):
    """
    DataStreamContext object.

    Parameters
    ----------
    context: Optional[List[Context]]
    created: Optional[datetime]
    datastream_name: Optional[constr(max_length=64, strict=True)]
    updated: Optional[datetime]

    """

    context: Optional[List[Context]] = Field(
        None,
        description="An array of objects associated with the Data Stream. Each object contains keys for the Asset `name` of the Asset / Data Stream pair and and the Source for the pair.",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Data Stream was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    datastream_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the Data Stream.", example="gas_flow_rate"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Data Stream keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )


class DataStreamContextGet(DataStreamContext):
    """
    DataStreamContextGet object.

    Parameters
    ----------

    """


class DataStreamContextsListPaginatedResponseCursor(PaginatorDataModel[DataStreamContext]):
    """
    DataStreamContextsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[DataStreamContext]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[DataStreamContext]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Streams and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataStreamContextsListPaginatedResponseLimits(PaginatorDataModel[DataStreamContext]):
    """
    DataStreamContextsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[DataStreamContext]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[DataStreamContext]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Streams and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataStreamContextsListPaginatedResponseStream(DataStreamContext):
    """
    DataStreamContextsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class DataTagCreate(DataTag):
    """
    DataTagCreate object.

    Parameters
    ----------

    """


class DataTagUpdate(DataTag):
    """
    DataTagUpdate object.

    Parameters
    ----------

    """


class DataTagGet(DataTag):
    """
    DataTagGet object.

    Parameters
    ----------

    """


class DataTagListPaginatedResponseCursor(PaginatorDataModel[type.DataTag]):
    """
    DataTagListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.DataTag]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.DataTag]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Tag objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class DataTagListPaginatedResponseLimits(PaginatorDataModel[type.DataTag]):
    """
    DataTagListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.DataTag]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.DataTag]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Data Tag objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class DataTagListPaginatedResponseStream(DataTag):
    """
    DataTagListPaginatedResponseStream object.

    Parameters
    ----------

    """


class TagCreate(Tag):
    """
    TagCreate object.

    Parameters
    ----------

    """


class TagUpdate(Tag):
    """
    TagUpdate object.

    Parameters
    ----------

    """


class TagGet(Tag):
    """
    TagGet object.

    Parameters
    ----------

    """


class TagListPaginatedResponseCursor(PaginatorDataModel[type.Tag]):
    """
    TagListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Tag]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Tag]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Tag objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class TagListPaginatedResponseLimits(PaginatorDataModel[type.Tag]):
    """
    TagListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Tag]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Tag]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Tag objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class TagListPaginatedResponseStream(Tag):
    """
    TagListPaginatedResponseStream object.

    Parameters
    ----------

    """


class FileUpload(FileStorage):
    """
    FileUpload object.

    Parameters
    ----------

    """


class FilesListPaginatedCursor(PaginatorDataModel[type.FileStorage]):
    """
    FilesListPaginatedCursor object.

    Parameters
    ----------
    data: Optional[List[type.FileStorage]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.FileStorage]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` file objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class FilesListPaginatedLimits(PaginatorDataModel[type.FileStorage]):
    """
    FilesListPaginatedLimits object.

    Parameters
    ----------
    data: Optional[List[type.FileStorage]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.FileStorage]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` file objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class FilesListPaginatedStream(FileStorage):
    """
    FilesListPaginatedStream object.

    Parameters
    ----------

    """


class FileGet(FileStorage):
    """
    FileGet object.

    Parameters
    ----------

    """


class GuardrailCreate(Guardrail):
    """
    GuardrailCreate object.

    Parameters
    ----------

    """


class GuardrailGet(Guardrail):
    """
    GuardrailGet object.

    Parameters
    ----------

    """


class GuardrailUpdate(Guardrail):
    """
    GuardrailUpdate object.

    Parameters
    ----------

    """


class GuardrailsListPaginatedResponseCursor(PaginatorDataModel[type.Guardrail]):
    """
    GuardrailsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Guardrail]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Guardrail]] = None
    pagination: Optional[pagination.PaginationCursor] = None


class GuardrailsListPaginatedResponseLimits(PaginatorDataModel[type.Guardrail]):
    """
    GuardrailsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Guardrail]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Guardrail]] = None
    pagination: Optional[pagination.PaginationLimits] = None


class GuardrailsListPaginatedResponseStream(Guardrail):
    """
    GuardrailsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class BulkGuardrailsCreate(DataModelBase):
    """
    BulkGuardrailsCreate object.

    Parameters
    ----------
    data: Optional[List[type.Guardrail]]

    """

    data: Optional[List[type.Guardrail]] = None


class InstanceAuditLogGetItem(InstanceAuditLogItem):
    """
    InstanceAuditLogGetItem object.

    Parameters
    ----------

    """


class InstanceAuditLogsListPaginatedResponseCursor(PaginatorDataModel[InstanceAuditLogGetItem]):
    """
    InstanceAuditLogsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[InstanceAuditLogGetItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[InstanceAuditLogGetItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Audit Log objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class InstanceAuditLogsListPaginatedResponseLimits(PaginatorDataModel[InstanceAuditLogGetItem]):
    """
    InstanceAuditLogsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[InstanceAuditLogGetItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[InstanceAuditLogGetItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Audit Log objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class InstanceAuditLogsListPaginatedResponseStream(InstanceAuditLogGetItem):
    """
    InstanceAuditLogsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class InstanceAuditLogGet(DataModelBase):
    """
    InstanceAuditLogGet object.

    Parameters
    ----------
    action: Optional[constr(min_length=1, max_length=64, strict=True)]
    created: Optional[datetime]
    id: Optional[StrictInt]
    identifier: Optional[constr(min_length=1, max_length=64, strict=True)]
    meta: Optional[Dict[str, Any]]
    namespace: Optional[constr(min_length=1, max_length=64, strict=True)]
    request_id: Optional[StrictStr]
    user_id: Optional[UUID]
    username: Optional[constr(min_length=1, max_length=64, strict=True)]

    """

    action: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="Type of action performed over the platform resource.", example="BATCH-UPDATE-NODE"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Audit Log was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    id: Optional[StrictInt] = Field(None, description="Unique ID of the Audit Log entry.", example=4739892)
    identifier: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="The platform resource that generated the audit log.", example="application_name"
    )
    meta: Optional[Dict[str, Any]] = Field(
        None,
        description="Contextual information about the action. For example, updating a resource you probably see information about the previous state (FROM key) and the current state (TO key) of the resource.",
    )
    namespace: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="In which service the audit log was created.", example="api-workload"
    )
    request_id: Optional[StrictStr] = Field(None, description="Deprecated. Not being used.")
    user_id: Optional[UUID] = Field(
        None, description="User ID that initiated the action.", example="0002bc79-b42f-461b-95d6-cf0a28ba87aa"
    )
    username: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="Username used to create the action.", example="service-account-node-client-aws-cluster"
    )


class InstanceSettingsAppManagerPlannerRulesGet(InstanceSettingsAppManagerPlannerRules):
    """
    InstanceSettingsAppManagerPlannerRulesGet object.

    Parameters
    ----------

    """


class InstanceSettingsAppManagerPlannerRulesUpdate(InstanceSettingsAppManagerPlannerRules):
    """
    InstanceSettingsAppManagerPlannerRulesUpdate object.

    Parameters
    ----------

    """


class InstanceSettingsKelvinClusterGet(InstanceSettings):
    """
    InstanceSettingsKelvinClusterGet object.

    Parameters
    ----------

    """


class InstanceSettingsKelvinClusterUpdate(InstanceSettings):
    """
    InstanceSettingsKelvinClusterUpdate object.

    Parameters
    ----------

    """


class InstanceSettingsListPaginatedResponseCursor(PaginatorDataModel[type.InstanceSettings]):
    """
    InstanceSettingsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.InstanceSettings]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.InstanceSettings]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Instance Setting objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class InstanceSettingsListPaginatedResponseLimits(PaginatorDataModel[type.InstanceSettings]):
    """
    InstanceSettingsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.InstanceSettings]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.InstanceSettings]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Instance Setting objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class InstanceSettingsListPaginatedResponseStream(InstanceSettings):
    """
    InstanceSettingsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class InstanceSettingsGet(InstanceSettings):
    """
    InstanceSettingsGet object.

    Parameters
    ----------

    """


class InstanceSettingsUpdate(InstanceSettings):
    """
    InstanceSettingsUpdate object.

    Parameters
    ----------

    """


class ComponentStatus(DataModelBase):
    """
    ComponentStatus object.

    Parameters
    ----------
    name: Optional[constr(min_length=1, max_length=64, strict=True)]
    status: Optional[StrictBool]

    """

    name: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="Name of service on the Instance.", example="api-workload"
    )
    status: Optional[StrictBool] = Field(
        None, description="Current status of the service on the Instance.", example=True
    )


class InstanceStatusGet(DataModelBase):
    """
    InstanceStatusGet object.

    Parameters
    ----------
    components: Optional[List[ComponentStatus]]
    status: Optional[StrictBool]

    """

    components: Optional[List[ComponentStatus]] = None
    status: Optional[StrictBool] = Field(None, description="Overall status of the Instance.", example=True)


class OrchestrationClustersCreate(OrchestrationCluster):
    """
    OrchestrationClustersCreate object.

    Parameters
    ----------

    """


class OrchestrationClustersCreateItem(DataModelBase):
    """
    OrchestrationClustersCreateItem object.

    Parameters
    ----------
    created: Optional[datetime]
    last_seen: Optional[datetime]
    name: Optional[constr(max_length=64, strict=True)]
    ready: Optional[StrictBool]
    status: Optional[enum.OrchestrationClusterStatus]
    title: Optional[constr(max_length=64, strict=True)]
    type: Optional[enum.ClusterType]
    updated: Optional[datetime]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Cluster was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Cluster was last seen by the Cloud, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Cluster.", example="aws-cluster"
    )
    ready: Optional[StrictBool] = Field(
        None, description="Setting to inform Kelvin UI if the Cluster is ready.", example=True
    )
    status: Optional[enum.OrchestrationClusterStatus] = None
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the Cluster.", example="AWS Cluster"
    )
    type: Optional[enum.ClusterType] = Field(
        None, description="Type of Cluster deployed. `k3s` is managed by Kelvin, `kubernetes` is managed by client."
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Cluster keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class OrchestrationClustersListPaginatedResponseCursor(PaginatorDataModel[OrchestrationClustersCreateItem]):
    """
    OrchestrationClustersListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[OrchestrationClustersCreateItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[OrchestrationClustersCreateItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Clusters and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class OrchestrationClustersListPaginatedResponseLimits(PaginatorDataModel[OrchestrationClustersCreateItem]):
    """
    OrchestrationClustersListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[OrchestrationClustersCreateItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[OrchestrationClustersCreateItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Clusters and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class OrchestrationClustersListPaginatedResponseStream(OrchestrationClustersCreateItem):
    """
    OrchestrationClustersListPaginatedResponseStream object.

    Parameters
    ----------

    """


class OrchestrationClustersGet(OrchestrationCluster):
    """
    OrchestrationClustersGet object.

    Parameters
    ----------

    """


class OrchestrationClustersCreateManifestImageItem(DataModelBase):
    """
    OrchestrationClustersCreateManifestImageItem object.

    Parameters
    ----------
    args: Optional[StrictStr]
    path: Optional[StrictStr]

    """

    args: Optional[StrictStr] = Field(None, description="Additional arguments for the image, if any.", example="--help")
    path: Optional[StrictStr] = Field(
        None, description="The path or location of the image.", example="<URL>/analysis-frame/<app-name>:{app-}"
    )


class OrchestrationClustersCreateManifestItem(DataModelBase):
    """
    OrchestrationClustersCreateManifestItem object.

    Parameters
    ----------
    content: Optional[StrictStr]
    file_name: Optional[StrictStr]

    """

    content: Optional[StrictStr] = Field(
        None, description="Base64 encoded content of the manifest file.", example="YXBpVmVyc2lvbj..."
    )
    file_name: Optional[StrictStr] = Field(None, description="Name of the manifest file.", example="certificate.yaml")


class OrchestrationClustersCreateManifestUpgrade(DataModelBase):
    """
    OrchestrationClustersCreateManifestUpgrade object.

    Parameters
    ----------
    download_type: Optional[StrictStr]
    upgrade_type: Optional[StrictStr]

    """

    download_type: Optional[StrictStr] = Field(
        None, description="Type of download process for the upgrade.", example="instantly"
    )
    upgrade_type: Optional[StrictStr] = Field(None, description="Type of upgrade process.", example="instantly")


class OrchestrationClustersManifestsGet(DataModelBase):
    """
    OrchestrationClustersManifestsGet object.

    Parameters
    ----------
    images: Optional[List[OrchestrationClustersCreateManifestImageItem]]
    manifests: Optional[List[OrchestrationClustersCreateManifestItem]]
    revision: Optional[StrictStr]
    upgrade: Optional[OrchestrationClustersCreateManifestUpgrade]

    """

    images: Optional[List[OrchestrationClustersCreateManifestImageItem]] = Field(
        None, description="List of images on the Cluster."
    )
    manifests: Optional[List[OrchestrationClustersCreateManifestItem]] = Field(
        None, description="List of Manifest files on the Cluster."
    )
    revision: Optional[StrictStr] = Field(
        None, description="Current Kelvin Software version installed on the Cluster.", example="4.0.0-rc2024.521"
    )
    upgrade: Optional[OrchestrationClustersCreateManifestUpgrade] = None


class OrchestrationClustersNodesGetItem(DataModelBase):
    """
    OrchestrationClustersNodesGetItem object.

    Parameters
    ----------
    created: Optional[datetime]
    last_seen: Optional[datetime]
    main: Optional[StrictBool]
    name: Optional[constr(max_length=64, strict=True)]
    status: Optional[enum.OrchestrationNodeStatus]
    updated: Optional[datetime]
    warnings: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Node was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Node was last seen by the Cloud, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    main: Optional[StrictBool] = Field(
        None, description="Whether the Node is the Master Node in the Cluster.", example=True
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Node.", example="internal-node-01"
    )
    status: Optional[enum.OrchestrationNodeStatus] = None
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Node keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    warnings: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None,
        description="Any warning messages received from Kubernetes.",
        example="container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized",
    )


class OrchestrationClustersNodeListPaginatedResponseCursor(PaginatorDataModel[OrchestrationClustersNodesGetItem]):
    """
    OrchestrationClustersNodeListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[OrchestrationClustersNodesGetItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[OrchestrationClustersNodesGetItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Nodes and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class OrchestrationClustersNodeListPaginatedResponseLimits(PaginatorDataModel[OrchestrationClustersNodesGetItem]):
    """
    OrchestrationClustersNodeListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[OrchestrationClustersNodesGetItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[OrchestrationClustersNodesGetItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Nodes and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class OrchestrationClustersNodeListPaginatedResponseStream(OrchestrationClustersNodesGetItem):
    """
    OrchestrationClustersNodeListPaginatedResponseStream object.

    Parameters
    ----------

    """


class OrchestrationClustersNodesGetConditionItem(DataModelBase):
    """
    OrchestrationClustersNodesGetConditionItem object.

    Parameters
    ----------
    lastHeartbeatTime: Optional[datetime]
    lastTransitionTime: Optional[datetime]
    message: Optional[StrictStr]
    name: Optional[StrictStr]
    reason: Optional[StrictStr]
    status: Optional[StrictStr]
    status_message: Optional[StrictStr]
    type: Optional[StrictStr]

    """

    lastHeartbeatTime: Optional[datetime] = Field(
        None, description="Timestamp of the last heartbeat received.", example="2024-01-20T12:34:56Z"
    )
    lastTransitionTime: Optional[datetime] = Field(
        None, description="Timestamp of the last status transition.", example="2024-01-19T11:30:00Z"
    )
    message: Optional[StrictStr] = Field(
        None,
        description="Human-readable message indicating details about the transition.",
        example="kubelet has no disk pressure",
    )
    name: Optional[StrictStr] = Field(
        None, description="Unique name identifying the resource.", example="Disk Pressure"
    )
    reason: Optional[StrictStr] = Field(
        None,
        description="Short, machine-understandable string that gives the reason for the condition's last transition.",
        example="KubeletHasNoDiskPressure",
    )
    status: Optional[StrictStr] = Field(
        None, description="Status of the condition, typically True, False, or Unknown.", example="False"
    )
    status_message: Optional[StrictStr] = Field(None, description="Detailed status message.", example="ready")
    type: Optional[StrictStr] = Field(None, description="Type of the condition.", example="DiskPressure")


class OrchestrationClustersNodesGetSystemInfo(DataModelBase):
    """
    OrchestrationClustersNodesGetSystemInfo object.

    Parameters
    ----------
    architecture: Optional[StrictStr]
    boot_id: Optional[StrictStr]
    container_runtime_version: Optional[StrictStr]
    host_name: Optional[StrictStr]
    kernel_version: Optional[StrictStr]
    kube_proxy_version: Optional[StrictStr]
    kubelet_version: Optional[StrictStr]
    machine_id: Optional[StrictStr]
    operating_system: Optional[StrictStr]
    os_image: Optional[StrictStr]
    system_uuid: Optional[StrictStr]

    """

    architecture: Optional[StrictStr] = Field(
        None, description="Architecture of the node's system (e.g., x86_64, arm).", example="amd64"
    )
    boot_id: Optional[StrictStr] = Field(
        None,
        description="Unique identifier for the current boot session.",
        example="c24e67a8-067f-462d-b569-12d06f700117",
    )
    container_runtime_version: Optional[StrictStr] = Field(
        None, description="Version of the container runtime.", example="containerd://1.6.15-k3s1"
    )
    host_name: Optional[StrictStr] = Field(None, description="Hostname of the node.", example="node01")
    kernel_version: Optional[StrictStr] = Field(
        None, description="Version of the node's kernel.", example="5.15.0-1050-aws"
    )
    kube_proxy_version: Optional[StrictStr] = Field(
        None, description="Version of kube-proxy running on the node.", example="v1.24.10+k3s1"
    )
    kubelet_version: Optional[StrictStr] = Field(
        None, description="Version of kubelet running on the node.", example="v1.24.10+k3s1"
    )
    machine_id: Optional[StrictStr] = Field(
        None, description="Unique identifier of the node's machine.", example="ec22bcece3288e3a08d7b7ce4b0742c1"
    )
    operating_system: Optional[StrictStr] = Field(
        None, description="Operating system running on the node.", example="linux"
    )
    os_image: Optional[StrictStr] = Field(
        None, description="Operating system image used on the node.", example="Ubuntu 22.04.3 LTS"
    )
    system_uuid: Optional[StrictStr] = Field(
        None, description="Universal unique identifier of the system.", example="ec22bcec-e328-8e3a-08d7-b7ce4b0742c1"
    )


class NetworkInfoItem(DataModelBase):
    """
    NetworkInfoItem object.

    Parameters
    ----------
    interface: Optional[StrictStr]
    ipv4: Optional[List[StrictStr]]
    ipv6: Optional[List[StrictStr]]
    dns: Optional[List[StrictStr]]

    """

    interface: Optional[StrictStr] = None
    ipv4: Optional[List[StrictStr]] = None
    ipv6: Optional[List[StrictStr]] = None
    dns: Optional[List[StrictStr]] = None


class OrchestrationClustersNodesGet(DataModelBase):
    """
    OrchestrationClustersNodesGet object.

    Parameters
    ----------
    capacity: Optional[Dict[str, Any]]
    conditions: Optional[List[OrchestrationClustersNodesGetConditionItem]]
    created: Optional[datetime]
    hostname: Optional[StrictStr]
    internal_ip: Optional[StrictStr]
    k8s_version: Optional[constr(max_length=64, strict=True)]
    labels: Optional[Dict[str, StrictStr]]
    last_seen: Optional[datetime]
    main: Optional[StrictBool]
    name: Optional[constr(max_length=64, strict=True)]
    network_info: Optional[List[NetworkInfoItem]]
    status: Optional[enum.OrchestrationNodeStatus]
    system_info: Optional[OrchestrationClustersNodesGetSystemInfo]
    updated: Optional[datetime]
    warnings: Optional[Dict[str, Any]]

    """

    capacity: Optional[Dict[str, Any]] = Field(
        None,
        description="UTC time when the Node was created, formatted in RFC 3339.",
        example={
            "cpu": "2",
            "ephemeral-storage": "30417472Ki",
            "hugepages-1Gi": "0",
            "hugepages-2Mi": "0",
            "memory": "3944492Ki",
            "pods": "110",
        },
    )
    conditions: Optional[List[OrchestrationClustersNodesGetConditionItem]] = Field(
        None, description="Detailed information about the Node's telemetry."
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Node was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    hostname: Optional[StrictStr] = Field(
        None,
        description="Name of a computer hosting Node. This name identifies the computer on the network.",
        example="node01",
    )
    internal_ip: Optional[StrictStr] = Field(
        None,
        description="Internal IP address of the computer. It's a unique address within the local network, typically starting with 192.168, 10, or 172.16 to 172.31.",
        example="192.168.1.10",
    )
    k8s_version: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Current version of k8s installed on the Cluster.", example="v1.24.10+k3s1"
    )
    labels: Optional[Dict[str, StrictStr]] = Field(
        None,
        description="Labels assigned to the Node.",
        example={
            "kubernetes.io/os": "linux",
            "node-role.kubernetes.io/control-plane": "true",
            "node-role.kubernetes.io/master": "true",
            "node.kubernetes.io/role": "acp",
        },
    )
    last_seen: Optional[datetime] = Field(
        None,
        description="UTC time when the Node was last seen by the Cloud, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    main: Optional[StrictBool] = Field(
        None, description="Whether the Node is the Master Node in the Cluster.", example=True
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Node.", example="aws-cluster-node-01"
    )
    network_info: Optional[List[NetworkInfoItem]] = Field(
        None,
        description="Details about the Node's current network settings.",
        example=[{"dns": [""], "interface": "ens5", "ipv4": ["172.31.40.200"], "ipv6": ["fe80::10d3:f3ff:fe1b:bea1"]}],
    )
    status: Optional[enum.OrchestrationNodeStatus] = None
    system_info: Optional[OrchestrationClustersNodesGetSystemInfo] = None
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Node keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    warnings: Optional[Dict[str, Any]] = Field(
        None,
        description="Any warning messages received from Kubernetes.",
        example="container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized",
    )


class ServiceType(Enum):
    cluster_ip = "cluster_ip"
    node_port = "node_port"
    host_port = "host_port"


class ServiceItem(DataModelBase):
    """
    ServiceItem object.

    Parameters
    ----------
    address: Optional[StrictStr]
    created: Optional[datetime]
    name: Optional[constr(max_length=32, strict=True)]
    network_interface: Optional[StrictStr]
    service_type: Optional[ServiceType]
    updated: Optional[datetime]
    workload_name: Optional[constr(max_length=32, strict=True)]

    """

    address: Optional[StrictStr] = Field(
        None, description="Address and port to connect to the Service.", example="opcua-se-0298b03c3fdbbe0.app:4842"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Service was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    name: Optional[constr(max_length=32, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Service.", example="opcua-se-0298b03c3fdbbe0"
    )
    network_interface: Optional[StrictStr] = Field(
        None, description="Physical network interface name of the Node hosting the Service.", example="kelvin"
    )
    service_type: Optional[ServiceType] = Field(
        None,
        description="Type of Service. `cluster_ip` restricts communication to within the cluster, not accessible externally. `node_port` makes the Service available on a static port across all Nodes. `host_port` exposes the Service on a designated port of the host Node only.",
        example="cluster_ip",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Service keys were last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    workload_name: Optional[constr(max_length=32, strict=True)] = Field(
        None, description="Unique identifier key `name` of the Node.", example="opcua-se-0298b03c3fdbbe0"
    )


class OrchestrationClustersServiceListPaginatedResponseCursor(PaginatorDataModel[ServiceItem]):
    """
    OrchestrationClustersServiceListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ServiceItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ServiceItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Nodes and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class OrchestrationClustersServiceListPaginatedResponseLimits(PaginatorDataModel[ServiceItem]):
    """
    OrchestrationClustersServiceListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ServiceItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ServiceItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Nodes and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class OrchestrationClustersServiceListPaginatedResponseStream(ServiceItem):
    """
    OrchestrationClustersServiceListPaginatedResponseStream object.

    Parameters
    ----------

    """


class OrchestrationClustersUpdate(OrchestrationCluster):
    """
    OrchestrationClustersUpdate object.

    Parameters
    ----------

    """


class ParameterValueItem(DataModelBase):
    """
    ParameterValueItem object.

    Parameters
    ----------
    app_name: Optional[constr(max_length=64, strict=True)]
    app_version: Optional[StrictStr]
    comment: Optional[constr(max_length=200, strict=True)]
    created: Optional[datetime]
    parameter_name: Optional[constr(max_length=64, strict=True)]
    resource: Optional[KRNAsset]
    source: Optional[KRN]
    updated: Optional[datetime]
    value: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]

    """

    app_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the App in the App Registry linked to this Parameter.",
        example="motor-speed-control",
    )
    app_version: Optional[StrictStr] = Field(
        None, description="Version number of the App in the App Registry linked to this Parameter.", example="1.2.0"
    )
    comment: Optional[constr(max_length=200, strict=True)] = Field(
        None,
        description="Latest information from user when creating or updating this Parameter.",
        example="updating parameter for well operational optimization.",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Parameter was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    parameter_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Parameter.", example="gas_flow_rate_max_threshold"
    )
    resource: Optional[KRNAsset] = Field(
        None, description="KRN of the Asset associated with the Parameter.", example="krn:asset:well_01"
    )
    source: Optional[KRN] = Field(
        None,
        description="KRN of the User or Service that last created or updated the Parameter.",
        example="krn:user:richard.teo@kelvininc.com",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Parameter keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    value: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None,
        description="The current value of the Parameter. The format returned will depend on the Primitive Type of the Parameter.",
        example=100,
    )


class ParametersAppVersionAssetListPaginatedResponseCursor(PaginatorDataModel[ParameterValueItem]):
    """
    ParametersAppVersionAssetListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ParameterValueItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ParameterValueItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ParametersAppVersionAssetListPaginatedResponseLimits(PaginatorDataModel[ParameterValueItem]):
    """
    ParametersAppVersionAssetListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ParameterValueItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ParameterValueItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ParametersAppVersionAssetListPaginatedResponseStream(ParameterValueItem):
    """
    ParametersAppVersionAssetListPaginatedResponseStream object.

    Parameters
    ----------

    """


class ParameterJSONSchemaProperties(DataModelBase):
    """
    ParameterJSONSchemaProperties object.

    Parameters
    ----------
    default: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    description: Optional[constr(max_length=200, strict=True)]
    examples: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    maxLength: Optional[StrictInt]
    maximum: Optional[StrictInt]
    minLength: Optional[StrictInt]
    minimum: Optional[StrictInt]
    pattern: Optional[StrictStr]
    title: Optional[constr(max_length=64, strict=True)]
    type: Optional[enum.DataType]
    enum: Optional[List[Union[StrictFloat, StrictStr, StrictBool]]]

    """

    default: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None, description="Default value or text for the Parameter in the App."
    )
    description: Optional[constr(max_length=200, strict=True)] = Field(
        None,
        description="Detailed description for this Parameter in the App.",
        example="Maximum allowable threshold for the gas flow through the pump system.",
    )
    examples: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = None
    maxLength: Optional[StrictInt] = Field(
        None,
        description="Maximum text length for the Parameter in the App. This ony applies to Parameters with a Primitive Type `string`.",
        example=64,
    )
    maximum: Optional[StrictInt] = Field(
        None,
        description="Maximum allowable value for the Parameter in the App. This ony applies to Parameters with a Primitive Type `number`.",
        example=100,
    )
    minLength: Optional[StrictInt] = Field(
        None,
        description="Minimum text length for the Parameter in the App. This ony applies to Parameters with a Primitive Type `string`.",
        example=1,
    )
    minimum: Optional[StrictInt] = Field(
        None,
        description="Minimum allowable value for the Parameter in the App. This ony applies to Parameters with a Primitive Type `number`.",
        example=50,
    )
    pattern: Optional[StrictStr] = Field(
        None,
        description="Allowable string combinations for the Parameter in the App. This ony applies to Parameters with a Primitive Type `string`.",
        example="^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$",
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Display name (`title`) of the Parameter in the App.", example="Gas Flow Max Threshold"
    )
    type: Optional[enum.DataType] = None
    enum: Optional[List[Union[StrictFloat, StrictStr, StrictBool]]] = Field(
        None, description="List of possible values for the Parameter in the App."
    )


class ParamtersAppVersionSchemaGet(DataModelBase):
    """
    ParamtersAppVersionSchemaGet object.

    Parameters
    ----------
    additionalProperties: Optional[StrictBool]
    properties: Optional[Dict[str, ParameterJSONSchemaProperties]]
    required: Optional[List[constr(min_length=1, max_length=64, strict=True)]]
    type: Optional[constr(max_length=64, strict=True)]

    """

    additionalProperties: Optional[StrictBool] = Field(
        None, description="Define if the App accepts additional Parameters.", example=False
    )
    properties: Optional[Dict[str, ParameterJSONSchemaProperties]] = Field(
        None,
        description="List of JSON ojbects with the App properties for each Parameter associated with the App.",
        example={
            "gas_flow_rate_max_threshold": {
                "default": 100,
                "description": "Maximum allowable threshold for the gas flow through the pump system.",
                "maximum": 100,
                "minimum": 50,
                "title": "Gas Flow Rate Max Threshold",
                "type": "number",
            },
            "gas_flow_rate_min_threshold": {
                "default": 50,
                "description": "Minimum allowable threshold for the gas flow through the pump system.",
                "maximum": 100,
                "minimum": 50,
                "title": "Gas Flow Rate Min Threshold",
                "type": "number",
            },
        },
    )
    required: Optional[List[constr(min_length=1, max_length=64, strict=True)]] = Field(
        None,
        description="Array of Parameter `name` keys that are mandatory for the App.",
        example=["gas_flow_rate_max_threshold", "gas_flow_rate_min_threshold"],
    )
    type: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Type of the key `properties` value. Currently it is always `object`.", example="object"
    )


class ParameterDefinitionItem(DataModelBase):
    """
    ParameterDefinitionItem object.

    Parameters
    ----------
    app_name: Optional[constr(max_length=64, strict=True)]
    created: Optional[datetime]
    last_title: Optional[constr(max_length=64, strict=True)]
    name: Optional[constr(max_length=64, strict=True)]
    primitive_type: Optional[enum.ParameterType]
    updated: Optional[datetime]

    """

    app_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the App in the App Registry linked to this Paramete Definition.",
        example="motor-speed-control",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Parameter Definition was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    last_title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Latest Display name (`title`) of the Parameter in the App.", example="Gas Flow Max Threshold"
    )
    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Parameter.", example="gas_flow_rate_max_threshold"
    )
    primitive_type: Optional[enum.ParameterType] = None
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Parameter Definition keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )


class ParametersDefinitionsListPaginatedResponseCursor(PaginatorDataModel[ParameterDefinitionItem]):
    """
    ParametersDefinitionsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ParameterDefinitionItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ParameterDefinitionItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter Definition objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ParametersDefinitionsListPaginatedResponseLimits(PaginatorDataModel[ParameterDefinitionItem]):
    """
    ParametersDefinitionsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ParameterDefinitionItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ParameterDefinitionItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter Definition objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ParametersDefinitionsListPaginatedResponseStream(ParameterDefinitionItem):
    """
    ParametersDefinitionsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class ParameterValueHistorianItem(DataModelBase):
    """
    ParameterValueHistorianItem object.

    Parameters
    ----------
    app_name: Optional[constr(max_length=64, strict=True)]
    app_version: Optional[StrictStr]
    comment: Optional[constr(max_length=200, strict=True)]
    created: Optional[datetime]
    parameter_name: Optional[constr(max_length=64, strict=True)]
    resource: Optional[KRNAsset]
    source: Optional[KRN]
    updated: Optional[datetime]
    value: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    invalidated: Optional[datetime]

    """

    app_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the App in the App Registry linked to this Parameter.",
        example="motor-speed-control",
    )
    app_version: Optional[StrictStr] = Field(
        None, description="Version number of the App in the App Registry linked to this Parameter.", example="1.2.0"
    )
    comment: Optional[constr(max_length=200, strict=True)] = Field(
        None,
        description="Latest information from user when creating or updating this Parameter.",
        example="updating parameter for well operational optimization.",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Parameter was first created, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    parameter_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Parameter.", example="gas_flow_rate_max_threshold"
    )
    resource: Optional[KRNAsset] = Field(
        None, description="KRN of the Asset associated with the Parameter.", example="krn:asset:well_01"
    )
    source: Optional[KRN] = Field(
        None,
        description="KRN of the User or Service that last created or updated the Parameter.",
        example="krn:user:richard.teo@kelvininc.com",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Parameter keys were last updated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )
    value: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None,
        description="The current value of the Parameter. The format returned will depend on the Primitive Type of the Parameter.",
        example=100,
    )
    invalidated: Optional[datetime] = Field(
        None,
        description="UTC time when any Parameter value were invalidated, formatted in RFC 3339.",
        example="2023-06-26T18:22:18.582724Z",
    )


class ResourceParametersListPaginatedResponseCursor(PaginatorDataModel[ParameterValueHistorianItem]):
    """
    ResourceParametersListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ParameterValueHistorianItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ParameterValueHistorianItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects and its current value for the related Resource, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ResourceParametersListPaginatedResponseLimits(PaginatorDataModel[ParameterValueHistorianItem]):
    """
    ResourceParametersListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ParameterValueHistorianItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ParameterValueHistorianItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects and its current value for the related Resource for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ResourceParametersListPaginatedResponseStream(ParameterValueHistorianItem):
    """
    ResourceParametersListPaginatedResponseStream object.

    Parameters
    ----------

    """


class LastParametersResourcesGetPaginatedResponseCursor(PaginatorDataModel[ParameterValueItem]):
    """
    LastParametersResourcesGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ParameterValueItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ParameterValueItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects and its current value for the related Resource, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class LastParametersResourcesGetPaginatedResponseLimits(PaginatorDataModel[ParameterValueItem]):
    """
    LastParametersResourcesGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ParameterValueItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ParameterValueItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects and its current value for the related Resource for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class LastParametersResourcesGetPaginatedResponseStream(ParameterValueItem):
    """
    LastParametersResourcesGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class ParametersValuesGet(DataModelBase):
    """
    ParametersValuesGet object.

    Parameters
    ----------
    app_parameter_values: Optional[Dict[str, Dict[str, List[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]]]]

    """

    app_parameter_values: Optional[
        Dict[str, Dict[str, List[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]]]
    ] = Field(
        None,
        description="Collection of objects where each object is an App containing an array of values for each Parameter that meets the request filter definitions. Only unique Parameter Values are shown, default values will not be shown.",
        example={
            "cp-temperature-producer": {"temperature_max_in_celsius": [111], "temperature_min_in_celsius": [69]},
            "demo-model": {"recommended_speed_setpoint": [120, 150, 90]},
        },
    )


class ParametersScheduleCreate(ParameterSchedule):
    """
    ParametersScheduleCreate object.

    Parameters
    ----------

    """


class ParametersScheduleGet(ParameterSchedule):
    """
    ParametersScheduleGet object.

    Parameters
    ----------

    """


class ParametersScheduleListPaginatedResponseCursor(PaginatorDataModel[ParametersScheduleGet]):
    """
    ParametersScheduleListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[ParametersScheduleGet]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[ParametersScheduleGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class ParametersScheduleListPaginatedResponseLimits(PaginatorDataModel[ParametersScheduleGet]):
    """
    ParametersScheduleListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[ParametersScheduleGet]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[ParametersScheduleGet]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Parameter objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class ParametersScheduleListPaginatedResponseStream(ParametersScheduleGet):
    """
    ParametersScheduleListPaginatedResponseStream object.

    Parameters
    ----------

    """


class RecommendationClustering(DataModelBase):
    """
    RecommendationClustering object.

    Parameters
    ----------
    count: Optional[StrictInt]
    recommendations_ids: Optional[List[UUID]]
    time_bucket_start: Optional[datetime]

    """

    count: Optional[StrictInt] = Field(
        None,
        description="Number of occurrences of Recommendations over the time period of `time_bucket` that meet the request parameters starting from time `time_bucket_start`.",
        example=2,
    )
    recommendations_ids: Optional[List[UUID]] = Field(
        None,
        description="An array of Recommendation `id`'s that have been counted.",
        example=["0002bc79-b42f-461b-95d6-cf0a28ba87aa", "518bcb79-ffaa-4d3f-8042-52634c34b71e"],
    )
    time_bucket_start: Optional[datetime] = Field(
        None,
        description="Time of the start of the count for the current `time_bucket` period in RFC 3339 UTC date/time format.",
        example="2023-11-18T18:22:18.582724Z",
    )


class RecommendationCreate(RecommendationActionStatus):
    """
    RecommendationCreate object.

    Parameters
    ----------

    """


class RecommendationLastGetPaginatedResponseCursor(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationLastGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Last Recommendation for each Asset and its associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RecommendationLastGetPaginatedResponseLimits(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationLastGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Last Recommendation for each Asset and its associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RecommendationLastGetPaginatedResponseStream(Recommendation):
    """
    RecommendationLastGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class RecommendationsListPaginatedResponseCursor(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendations and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RecommendationsListPaginatedResponseLimits(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendations and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RecommendationsListPaginatedResponseStream(Recommendation):
    """
    RecommendationsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class RecommendationRangeGetPaginatedResponseCursor(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationRangeGetPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendation for each Asset and its associated context objects over the time range, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RecommendationRangeGetPaginatedResponseLimits(PaginatorDataModel[type.Recommendation]):
    """
    RecommendationRangeGetPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.Recommendation]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.Recommendation]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendations for each Asset and its associated context objects over the time range for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RecommendationRangeGetPaginatedResponseStream(Recommendation):
    """
    RecommendationRangeGetPaginatedResponseStream object.

    Parameters
    ----------

    """


class RecommendationTypeCreate(RecommendationType):
    """
    RecommendationTypeCreate object.

    Parameters
    ----------

    """


class RecommendationTypesListPaginatedCursor(PaginatorDataModel[type.RecommendationType]):
    """
    RecommendationTypesListPaginatedCursor object.

    Parameters
    ----------
    data: Optional[List[type.RecommendationType]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.RecommendationType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendation Types and associated context objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RecommendationTypesListPaginatedLimits(PaginatorDataModel[type.RecommendationType]):
    """
    RecommendationTypesListPaginatedLimits object.

    Parameters
    ----------
    data: Optional[List[type.RecommendationType]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.RecommendationType]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Recommendation Types and associated context objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RecommendationTypesListPaginatedStream(RecommendationType):
    """
    RecommendationTypesListPaginatedStream object.

    Parameters
    ----------

    """


class RecommendationTypeGet(RecommendationType):
    """
    RecommendationTypeGet object.

    Parameters
    ----------

    """


class RecommendationTypeUpdate(RecommendationType):
    """
    RecommendationTypeUpdate object.

    Parameters
    ----------

    """


class RecommendationAcceptUpdate(RecommendationActionStatus):
    """
    RecommendationAcceptUpdate object.

    Parameters
    ----------

    """


class RecommendationDelete(RecommendationActionStatus):
    """
    RecommendationDelete object.

    Parameters
    ----------

    """


class RecommendationGet(Recommendation):
    """
    RecommendationGet object.

    Parameters
    ----------

    """


class RecommendationRejectUpdate(RecommendationActionStatus):
    """
    RecommendationRejectUpdate object.

    Parameters
    ----------

    """


class SecretCreate(DataModelBase):
    """
    SecretCreate object.

    Parameters
    ----------
    name: Optional[constr(max_length=32, strict=True)]

    """

    name: Optional[constr(max_length=32, strict=True)] = Field(
        None,
        description="Unique identifier `name` for the Secret. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="secret_password",
    )


class SecretItem(DataModelBase):
    """
    SecretItem object.

    Parameters
    ----------
    name: Optional[constr(max_length=32, strict=True)]

    """

    name: Optional[constr(max_length=32, strict=True)] = Field(
        None,
        description="Unique identifier `name` for the Secret. The string can only contain lowercase alphanumeric characters and `.`, `_` or `-` characters.",
        example="secret_password",
    )


class SecretsListPaginatedResponseCursor(PaginatorDataModel[SecretItem]):
    """
    SecretsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[SecretItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[SecretItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Secret objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class SecretsListPaginatedResponseLimits(PaginatorDataModel[SecretItem]):
    """
    SecretsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[SecretItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[SecretItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Secret objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class SecretsListPaginatedResponseStream(SecretItem):
    """
    SecretsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class TimeseriesLastGet(TimeseriesData):
    """
    TimeseriesLastGet object.

    Parameters
    ----------

    """


class TimeseriesListPaginatedResponseCursor(PaginatorDataModel[type.TimeseriesData]):
    """
    TimeseriesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.TimeseriesData]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.TimeseriesData]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Time Series objects, starting from the index specified by the pagination parameters. Each object is a separate last value that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class TimeseriesListPaginatedResponseLimits(PaginatorDataModel[type.TimeseriesData]):
    """
    TimeseriesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.TimeseriesData]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.TimeseriesData]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Time Series objects for the page number specified by the pagination parameters. Each object is a separate last value that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class TimeseriesListPaginatedResponseStream(TimeseriesData):
    """
    TimeseriesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class TimeseriesRangeGet(DataModelBase):
    """
    TimeseriesRangeGet object.

    Parameters
    ----------
    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]
    resource: Optional[KRNAssetDataStream]
    timestamp: Optional[datetime]

    """

    payload: Optional[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]] = Field(
        None, description="Raw or aggregate value for `resource` at the specified `timestamp`."
    )
    resource: Optional[KRNAssetDataStream] = Field(
        None,
        description="The `resource` (Asset / Data Stream pair) associated with the `payload`.",
        example="krn:ad:asset1/data_stream1",
    )
    timestamp: Optional[datetime] = Field(
        None,
        description="UTC time when the `payload` values were saved, formatted in RFC 3339.",
        example="2023-11-13T12:00:00Z",
    )


class UserItem(DataModelBase):
    """
    UserItem object.

    Parameters
    ----------
    created: Optional[datetime]
    email: Optional[EmailStr]
    first_name: Optional[constr(max_length=64, strict=True)]
    id: Optional[UUID]
    last_name: Optional[constr(max_length=64, strict=True)]
    username: Optional[constr(max_length=64, strict=True)]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the User was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    email: Optional[EmailStr] = Field(None, description="Email of the user.", example="john.doe@kelvin.ai")
    first_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="First name of the User.", example="John"
    )
    id: Optional[UUID] = Field(
        None,
        description="A unique random generated UUID as the key `id` for the User.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    last_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Last name of the User.", example="Doe"
    )
    username: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Username of the User.", example="johndoe"
    )


class UsersListPaginatedResponseCursor(PaginatorDataModel[UserItem]):
    """
    UsersListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[UserItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[UserItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` User objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class UsersListPaginatedResponseLimits(PaginatorDataModel[UserItem]):
    """
    UsersListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[UserItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[UserItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` User objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class UsersListPaginatedResponseStream(UserItem):
    """
    UsersListPaginatedResponseStream object.

    Parameters
    ----------

    """


class UserMeGet(DataModelBase):
    """
    UserMeGet object.

    Parameters
    ----------
    created: Optional[datetime]
    email: Optional[EmailStr]
    first_name: Optional[constr(max_length=64, strict=True)]
    id: Optional[UUID]
    last_name: Optional[constr(max_length=64, strict=True)]
    permissions: Optional[List[constr(min_length=1, max_length=64, strict=True)]]
    groups: Optional[List[StrictStr]]
    username: Optional[constr(max_length=64, strict=True)]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the current User was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    email: Optional[EmailStr] = Field(None, description="Email of the current user.", example="john.doe@kelvin.ai")
    first_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="First name of the current User.", example="John"
    )
    id: Optional[UUID] = Field(
        None,
        description="A unique random generated UUID as the key `id` for the current User.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    last_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Last name of the current User.", example="Doe"
    )
    permissions: Optional[List[constr(min_length=1, max_length=64, strict=True)]] = Field(
        None,
        description="Lists all Instance permissions accessible to the current User.",
        example=[
            "kelvin.permission.bridge.update",
            "kelvin.permission.appmanager.delete",
            "kelvin.permission.asset.delete",
        ],
    )
    groups: Optional[List[StrictStr]] = Field(
        None, description="Lists of all groups the current User belongs to.", example=["my_group"]
    )
    username: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Username of the current User.", example="johndoe"
    )


class UserSettingsListPaginatedResponseCursor(PaginatorDataModel[type.UserSetting]):
    """
    UserSettingsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[type.UserSetting]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[type.UserSetting]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` User Setting objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class UserSettingsListPaginatedResponseLimits(PaginatorDataModel[type.UserSetting]):
    """
    UserSettingsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[type.UserSetting]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[type.UserSetting]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` User Setting objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class UserSettingsListPaginatedResponseStream(UserSetting):
    """
    UserSettingsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class UserSettingsGet(UserSetting):
    """
    UserSettingsGet object.

    Parameters
    ----------

    """


class UserSettingsUpdate(UserSetting):
    """
    UserSettingsUpdate object.

    Parameters
    ----------

    """


class UserGet(DataModelBase):
    """
    UserGet object.

    Parameters
    ----------
    created: Optional[datetime]
    email: Optional[EmailStr]
    first_name: Optional[constr(min_length=1, max_length=64, strict=True)]
    id: Optional[UUID]
    last_name: Optional[constr(min_length=1, max_length=64, strict=True)]
    username: Optional[constr(min_length=1, max_length=64, strict=True)]

    """

    created: Optional[datetime] = Field(
        None,
        description="UTC time when the User was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    email: Optional[EmailStr] = Field(None, description="Email of the user.", example="john.doe@kelvin.ai")
    first_name: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="First name of the User.", example="John"
    )
    id: Optional[UUID] = Field(
        None,
        description="A unique random generated UUID as the key `id` for the User.",
        example="0002bc79-b42f-461b-95d6-cf0a28ba87aa",
    )
    last_name: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="Last name of the User.", example="Doe"
    )
    username: Optional[constr(min_length=1, max_length=64, strict=True)] = Field(
        None, description="Username of the User.", example="johndoe"
    )


class Role(DataModelBase):
    """
    Role object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Role.", example="my_role"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Role.", example="My Role"
    )


class Group(DataModelBase):
    """
    Group object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]
    description: Optional[constr(max_length=256, strict=True)]
    roles: Optional[List[Role]]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Group.", example="my_group"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Group.", example="My Group"
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None, description="The description of the Group.          ", example="This is my group"
    )
    roles: Optional[List[Role]] = Field(None, description="A list of role objects that the group belongs to.")
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Group was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Group was last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class GroupCreate(Group):
    """
    GroupCreate object.

    Parameters
    ----------

    """


class GroupItem(DataModelBase):
    """
    GroupItem object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]
    description: Optional[constr(max_length=256, strict=True)]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Group.", example="my_group"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Group.", example="My Group"
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None, description="The description of the Group.          ", example="This is my group"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Group was created, formatted in RFC 3339.          ",
        example="2023-11-18T18:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Group was last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class GroupsListPaginatedResponseCursor(PaginatorDataModel[GroupItem]):
    """
    GroupsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[GroupItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[GroupItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Group objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class GroupsListPaginatedResponseLimits(PaginatorDataModel[GroupItem]):
    """
    GroupsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[GroupItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[GroupItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Group objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class GroupsListPaginatedResponseStream(GroupItem):
    """
    GroupsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class GroupGet(Group):
    """
    GroupGet object.

    Parameters
    ----------

    """


class GroupUpdate(Group):
    """
    GroupUpdate object.

    Parameters
    ----------

    """


class GroupModel(DataModelBase):
    """
    GroupModel object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Group.", example="my_group"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Group.", example="My Group"
    )


class RoleModel(DataModelBase):
    """
    RoleModel object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]
    description: Optional[constr(max_length=256, strict=True)]
    groups: Optional[List[GroupModel]]
    updated: Optional[datetime]
    created: Optional[datetime]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Role.", example="my_role"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Role.", example="My Role"
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None, description="The description of the Role.", example="This is my role"
    )
    groups: Optional[List[GroupModel]] = Field(None, description="A list of group objects that the role belongs to.")
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Role was last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Role was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class RoleCreate(RoleModel):
    """
    RoleCreate object.

    Parameters
    ----------

    """


class RoleItem(DataModelBase):
    """
    RoleItem object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    title: Optional[constr(max_length=64, strict=True)]
    description: Optional[constr(max_length=256, strict=True)]
    policy_names: Optional[List[constr(max_length=64, strict=True)]]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Role.", example="my_role"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Role.", example="My Role"
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None, description="The description of the Role.", example="This is my role"
    )
    policy_names: Optional[List[constr(max_length=64, strict=True)]] = None
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Role was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Role was last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class RolesListPaginatedResponseCursor(PaginatorDataModel[RoleItem]):
    """
    RolesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[RoleItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[RoleItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Role objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RolesListPaginatedResponseLimits(PaginatorDataModel[RoleItem]):
    """
    RolesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[RoleItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[RoleItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Role objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RolesListPaginatedResponseStream(RoleItem):
    """
    RolesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class RoleGet(RoleModel):
    """
    RoleGet object.

    Parameters
    ----------

    """


class RoleUpdate(RoleModel):
    """
    RoleUpdate object.

    Parameters
    ----------

    """


class Rule(DataModelBase):
    """
    Rule object.

    Parameters
    ----------
    actions: Optional[List[enum.RolePolicyAction]]
    condition: Optional[type.RolePolicyCondition]

    """

    actions: Optional[List[enum.RolePolicyAction]] = None
    condition: Optional[type.RolePolicyCondition] = None


class RolePolicy(DataModelBase):
    """
    RolePolicy object.

    Parameters
    ----------
    name: Optional[constr(max_length=64, strict=True)]
    resource_type: Optional[enum.ResourceType]
    title: Optional[constr(max_length=64, strict=True)]
    description: Optional[constr(max_length=256, strict=True)]
    rule: Optional[Rule]
    created: Optional[datetime]
    updated: Optional[datetime]

    """

    name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The name of the Policy.", example="my_policy"
    )
    resource_type: Optional[enum.ResourceType] = Field(
        None, description="The resource_type to which the policy applies.", example="asset"
    )
    title: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="The title of the Policy.", example="My Policy"
    )
    description: Optional[constr(max_length=256, strict=True)] = Field(
        None, description="The description of the Policy.", example="This is my policy"
    )
    rule: Optional[Rule] = None
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Policy was created, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when the Policy was last updated, formatted in RFC 3339.",
        example="2023-11-18T18:22:18.582724Z",
    )


class RolePolicyCreate(RolePolicy):
    """
    RolePolicyCreate object.

    Parameters
    ----------

    """


class RolePoliciesListPaginatedResponseCursor(PaginatorDataModel[RolePolicy]):
    """
    RolePoliciesListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[RolePolicy]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[RolePolicy]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Role Policy objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class RolePoliciesListPaginatedResponseLimits(PaginatorDataModel[RolePolicy]):
    """
    RolePoliciesListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[RolePolicy]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[RolePolicy]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Role Policy objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class RolePoliciesListPaginatedResponseStream(RolePolicy):
    """
    RolePoliciesListPaginatedResponseStream object.

    Parameters
    ----------

    """


class RolePolicyGet(RolePolicy):
    """
    RolePolicyGet object.

    Parameters
    ----------

    """


class RolePolicyUpdate(RolePolicy):
    """
    RolePolicyUpdate object.

    Parameters
    ----------

    """


class WorkloadDeploy(Workload):
    """
    WorkloadDeploy object.

    Parameters
    ----------

    """


class Staged(DataModelBase):
    """
    Staged object.

    Parameters
    ----------
    ready: Optional[StrictBool]
    app_version: Optional[StrictStr]
    status: Optional[type.StagedStatus]

    """

    ready: Optional[StrictBool] = Field(None, description="Staged workload ready to be applied.", example=True)
    app_version: Optional[StrictStr] = Field(
        None, description="Version Number of the Kelvin App used for the Staged Workload.", example="1.2.0"
    )
    status: Optional[type.StagedStatus] = None


class WorkloadItem(DataModelBase):
    """
    WorkloadItem object.

    Parameters
    ----------
    acp_name: Optional[constr(max_length=64, strict=True)]
    app_name: Optional[constr(max_length=64, strict=True)]
    app_version: Optional[StrictStr]
    cluster_name: Optional[constr(max_length=64, strict=True)]
    created: Optional[datetime]
    download_status: Optional[enum.WorkloadDownloadStatus]
    download_error: Optional[StrictStr]
    enabled: Optional[StrictBool]
    instantly_apply: Optional[StrictBool]
    name: Optional[constr(max_length=32, strict=True)]
    node_name: Optional[constr(max_length=64, strict=True)]
    pre_download: Optional[StrictBool]
    status: Optional[type.WorkloadStatus]
    title: Optional[StrictStr]
    updated: Optional[datetime]
    staged: Optional[Staged]

    """

    acp_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="[`Deprecated`] Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    app_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Kelvin App in the App Registry.",
        example="motor-speed-control",
    )
    app_version: Optional[StrictStr] = Field(
        None, description="Version Number of the Kelvin App used for this Workload.", example="1.2.0"
    )
    cluster_name: Optional[constr(max_length=64, strict=True)] = Field(
        None, description="Unique identifier `name` of the Cluster.", example="docs-demo-cluster-k3s"
    )
    created: Optional[datetime] = Field(
        None,
        description="UTC time when the Workload was first created, formatted in RFC 3339.",
        example="2023-12-26T18:22:18.582724Z",
    )
    download_status: Optional[enum.WorkloadDownloadStatus] = None
    download_error: Optional[StrictStr] = Field(
        None,
        description="Simple description of the error in case the image download failed.",
        example="an error occurred while saving the image",
    )
    enabled: Optional[StrictBool] = Field(
        None,
        description="If true, Workload `status` is set to `running` and will process I/O's. If false, Workload `status` is set to `stopped` but remains in Node on the Edge System.",
        example=True,
    )
    instantly_apply: Optional[StrictBool] = Field(
        None,
        description="If true, applies deploy/upgrade immediately. If false, user will need to send an additional API request `/workloads/{workload_name}/apply` to initate the deploy/upgrade.",
        example=True,
    )
    name: Optional[constr(max_length=32, strict=True)] = Field(
        None, description="Unique identifier `name` of the Workload.", example="motor-speed-control-ubdhwnshdy67"
    )
    node_name: Optional[constr(max_length=64, strict=True)] = Field(
        None,
        description="Unique identifier `name` of the Node in the Cluster hosting the Workload.",
        example="docs-demo-node-01",
    )
    pre_download: Optional[StrictBool] = Field(
        None,
        description="If true, deploy process is handled by Kelvin and all Workloads wil be downloaded to Edge System before deploy. If false, deploy process is handled by Kubernetes through default settings.",
        example=True,
    )
    status: Optional[type.WorkloadStatus] = None
    title: Optional[StrictStr] = Field(
        None, description="Display name (`title`) of the Workload.", example="Motor Speed Control"
    )
    updated: Optional[datetime] = Field(
        None,
        description="UTC time when any Workload keys were last updated, formatted in RFC 3339.",
        example="2023-12-18T18:22:18.582724Z",
    )
    staged: Optional[Staged] = None


class WorkloadsListPaginatedResponseCursor(PaginatorDataModel[WorkloadItem]):
    """
    WorkloadsListPaginatedResponseCursor object.

    Parameters
    ----------
    data: Optional[List[WorkloadItem]]
    pagination: Optional[pagination.PaginationCursor]

    """

    data: Optional[List[WorkloadItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Workload objects, starting from the index specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationCursor] = None


class WorkloadsListPaginatedResponseLimits(PaginatorDataModel[WorkloadItem]):
    """
    WorkloadsListPaginatedResponseLimits object.

    Parameters
    ----------
    data: Optional[List[WorkloadItem]]
    pagination: Optional[pagination.PaginationLimits]

    """

    data: Optional[List[WorkloadItem]] = Field(
        None,
        description="A dictionary with a data property that contains an array of up to `page_size` Workload objects for the page number specified by the pagination parameters, that matches the query parameters.",
    )
    pagination: Optional[pagination.PaginationLimits] = None


class WorkloadsListPaginatedResponseStream(WorkloadItem):
    """
    WorkloadsListPaginatedResponseStream object.

    Parameters
    ----------

    """


class WorkloadConfigurationGet(DataModelBase):
    """
    WorkloadConfigurationGet object.

    Parameters
    ----------
    configuration: Optional[Dict[str, Any]]

    """

    configuration: Optional[Dict[str, Any]] = None


class WorkloadConfigurationUpdate(DataModelBase):
    """
    WorkloadConfigurationUpdate object.

    Parameters
    ----------
    configuration: Optional[Dict[str, Any]]

    """

    configuration: Optional[Dict[str, Any]] = None


class WorkloadDownload(DataModelBase):
    """
    WorkloadDownload object.

    Parameters
    ----------
    url: Optional[StrictStr]
    expires_in: Optional[StrictInt]

    """

    url: Optional[StrictStr] = Field(None, description="URL to download the Workload package file.")
    expires_in: Optional[StrictInt] = Field(None, description="Time in seconds before the URL expires.")


class WorkloadGet(Workload):
    """
    WorkloadGet object.

    Parameters
    ----------

    """


class WorkloadLogsGet(DataModelBase):
    """
    WorkloadLogsGet object.

    Parameters
    ----------
    logs: Optional[Dict[str, List[StrictStr]]]

    """

    logs: Optional[Dict[str, List[StrictStr]]] = Field(
        None,
        example={
            "bp-opcua-bridge-0": [
                '2023-12-20T13:57:38.466076008Z {"asset":"bp_33","event":"Casted message from Float64 variant"}',
                '2023-12-20T13:57:38.466198095Z {"event":"[Runtime.cpp: 626:D] - publishing:  choke_position_set_point"}',
            ]
        },
    )


class ThreadsList(BaseModelRoot[List[type.Thread]]):
    """
    ThreadsList object.

    Parameters
    ----------
    __root__: List[type.Thread]

    """

    __root__: List[type.Thread]


class ThreadCreate(Thread):
    """
    ThreadCreate object.

    Parameters
    ----------

    """


class ThreadFollowUpdate(Thread):
    """
    ThreadFollowUpdate object.

    Parameters
    ----------

    """


class ThreadGet(Thread):
    """
    ThreadGet object.

    Parameters
    ----------

    """


class ThreadReplyCreate(Thread):
    """
    ThreadReplyCreate object.

    Parameters
    ----------

    """


class ThreadReplyUpdate(Thread):
    """
    ThreadReplyUpdate object.

    Parameters
    ----------

    """


class ThreadSeenUpdate(Thread):
    """
    ThreadSeenUpdate object.

    Parameters
    ----------

    """


class ThreadUpdate(Thread):
    """
    ThreadUpdate object.

    Parameters
    ----------

    """
