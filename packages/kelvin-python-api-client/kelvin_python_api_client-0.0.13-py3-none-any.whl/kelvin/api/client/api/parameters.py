"""
Kelvin API Client.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, Union, cast

from typing_extensions import Literal

from kelvin.api.client.api_service_model import ApiServiceModel
from kelvin.api.client.data_model import KList

from ..model import requests, response, responses


class Parameters(ApiServiceModel):
    @classmethod
    def list_parameters_app_version_asset(
        cls,
        app_name: str,
        version: str,
        asset_name: str,
        search: Optional[Sequence[str]] = None,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
    ) -> Union[KList[responses.ParameterValueItem], responses.ParametersAppVersionAssetListPaginatedResponseCursor]:
        """
        List Asset App Version Parameters lists the app version asset parameters.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``listParametersAppVersionAsset``: ``GET`` ``/api/v4/parameters/app/{app_name}/versions/{version}/assets/{asset_name}/list``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            A filter on the list based on the key `app_name`. The filter is on the
            full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters.
        version : :obj:`str`, optional
            A filter on the list based on the key `app_version`. The filter is on
            the full value only. The string can only contain lowercase
            alphanumeric characters and `.`, `_` or `-` characters.
        asset_name : :obj:`str`, optional
            A filter on the list based on the Asset Name in the key `resource`. Do
            not use the `krn` format, only the Asset Name itself. The filter is on
            the full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters.
        search : :obj:`Sequence[str]`
        pagination_type : :obj:`Literal['limits', 'cursor', 'stream']`
            Method of pagination to use for return results where `total_items` is
            greater than `page_size`. `cursor` and `limits` will return one `page`
            of results, `stream` will return all results. ('limits', 'cursor',
            'stream')
        page_size : :obj:`int`
            Number of objects to be returned in each page. Page size can range
            between 1 and 1000 objects.
        page : :obj:`int`
            An integer for the wanted page of results. Used only with
            `pagination_type` set as `limits`.
        next : :obj:`str`
            An alphanumeric string bookmark to indicate where to start for the
            next page. Used only with `pagination_type` set as `cursor`.
        previous : :obj:`str`
            An alphanumeric string bookmark to indicate where to end for the
            previous page. Used only with `pagination_type` set as `cursor`.
        direction : :obj:`Literal['asc', 'desc']`
            Sorting order according to the `sort_by` parameter. ('asc', 'desc')
        sort_by : :obj:`Sequence[str]`
            Sort the results by one or more enumerators.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/parameters/app/{app_name}/versions/{version}/assets/{asset_name}/list",
            {"app_name": app_name, "version": version, "asset_name": asset_name},
            {
                "search": search,
                "pagination_type": pagination_type,
                "page_size": page_size,
                "page": page,
                "next": next,
                "previous": previous,
                "direction": direction,
                "sort_by": sort_by,
            },
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.ParametersAppVersionAssetListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
        )
        return (
            cast(
                Union[
                    KList[responses.ParameterValueItem], responses.ParametersAppVersionAssetListPaginatedResponseCursor
                ],
                cls.fetch(
                    _client,
                    "/api/v4/parameters/app/{app_name}/versions/{version}/assets/{asset_name}/list",
                    result,
                    "GET",
                ),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def update_parameters(
        cls,
        app_name: str,
        version: str,
        asset_name: str,
        data: Optional[Union[requests.ParametersUpdate, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Update the value of one or more Parameters in an App.

        **Permission Required:** `kelvin.permission.parameter.update`.

        ``updateParameters``: ``POST`` ``/api/v4/parameters/app/{app_name}/versions/{version}/assets/{asset_name}/update``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            App name in the key `app_name`. The string can only contain lowercase
            alphanumeric characters and `.`, `_` or `-` characters.
        version : :obj:`str`, optional
            App Version in the key `app_version`.
        asset_name : :obj:`str`, optional
            Asset Name in the key `resource`. Do not use the `krn` format, only
            the Asset Name itself. The string can only contain lowercase
            alphanumeric characters and `.`, `_` or `-` characters.
        data: requests.ParametersUpdate, optional
        **kwargs:
            Extra parameters for requests.ParametersUpdate
              - update_parameters: dict

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/app/{app_name}/versions/{version}/assets/{asset_name}/update",
            {"app_name": app_name, "version": version, "asset_name": asset_name},
            {},
            {},
            {},
            data,
            "requests.ParametersUpdate",
            False,
            {"200": None, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def get_paramters_app_version_schema(
        cls, app_name: str, version: str, _dry_run: bool = False, _client: Any = None
    ) -> responses.ParamtersAppVersionSchemaGet:
        """
        Get the properties of each Parameter associated with an App.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``getParamtersAppVersionSchema``: ``GET`` ``/api/v4/parameters/app/{app_name}/versions/{version}/schema/get``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Parameter key `app_name` to retrieve. The string can only contain
            lowercase alphanumeric characters and `.`, `_` or `-` characters.
        version : :obj:`str`, optional
            Parameter key `app_version` to retireve.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/parameters/app/{app_name}/versions/{version}/schema/get",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.ParamtersAppVersionSchemaGet,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def update_paramters_app_version(
        cls,
        app_name: str,
        version: str,
        data: Optional[Union[requests.ParamtersAppVersionUpdate, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Bulk update Parameters for multiple resources of a given App Version.
        Parameters belonging to the App Version but not specified in the payload
        will **not** be changed. Setting a value to `null` will cause the parameter
        to be unset.  Additionally, it's also possible to set a comment for each
        parameter change.

        The source of the change will, by default, be the user making the API
        request. If the user making the request is a Service Account, it can,
        optionally, set its own source KRN.

        ``updateParamtersAppVersion``: ``POST`` ``/api/v4/parameters/app/{app_name}/versions/{version}/update``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            App name
        version : :obj:`str`, optional
            App version
        data: requests.ParamtersAppVersionUpdate, optional
        **kwargs:
            Extra parameters for requests.ParamtersAppVersionUpdate
              - update_paramters_app_version: dict

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/app/{app_name}/versions/{version}/update",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            data,
            "requests.ParamtersAppVersionUpdate",
            False,
            {"200": None, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def list_parameters_definitions(
        cls,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.ParametersDefinitionsList, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[responses.ParameterDefinitionItem], responses.ParametersDefinitionsListPaginatedResponseCursor]:
        """
        Returns a list of Parameters and its definition in each App. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``listParametersDefinitions``: ``POST`` ``/api/v4/parameters/definitions/list``

        Parameters
        ----------
        pagination_type : :obj:`Literal['limits', 'cursor', 'stream']`
            Method of pagination to use for return results where `total_items` is
            greater than `page_size`. `cursor` and `limits` will return one `page`
            of results, `stream` will return all results. ('limits', 'cursor',
            'stream')
        page_size : :obj:`int`
            Number of objects to be returned in each page. Page size can range
            between 1 and 1000 objects.
        page : :obj:`int`
            An integer for the wanted page of results. Used only with
            `pagination_type` set as `limits`.
        next : :obj:`str`
            An alphanumeric string bookmark to indicate where to start for the
            next page. Used only with `pagination_type` set as `cursor`.
        previous : :obj:`str`
            An alphanumeric string bookmark to indicate where to end for the
            previous page. Used only with `pagination_type` set as `cursor`.
        direction : :obj:`Literal['asc', 'desc']`
            Sorting order according to the `sort_by` parameter. ('asc', 'desc')
        sort_by : :obj:`Sequence[str]`
            Sort the results by one or more enumerators.
        data: requests.ParametersDefinitionsList, optional
        **kwargs:
            Extra parameters for requests.ParametersDefinitionsList
              - list_parameters_definitions: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/definitions/list",
            {},
            {
                "pagination_type": pagination_type,
                "page_size": page_size,
                "page": page,
                "next": next,
                "previous": previous,
                "direction": direction,
                "sort_by": sort_by,
            },
            {},
            {},
            data,
            "requests.ParametersDefinitionsList",
            False,
            {
                "200": responses.ParametersDefinitionsListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[
                    KList[responses.ParameterDefinitionItem], responses.ParametersDefinitionsListPaginatedResponseCursor
                ],
                cls.fetch(_client, "/api/v4/parameters/definitions/list", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def get_last_parameters_resources(
        cls,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.LastParametersResourcesGet, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[responses.ParameterValueItem], responses.LastParametersResourcesGetPaginatedResponseCursor]:
        """
        Returns the current value of Parameters for each Resource. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``getLastParametersResources``: ``POST`` ``/api/v4/parameters/resources/last/get``

        Parameters
        ----------
        pagination_type : :obj:`Literal['limits', 'cursor', 'stream']`
            Method of pagination to use for return results where `total_items` is
            greater than `page_size`. `cursor` and `limits` will return one `page`
            of results, `stream` will return all results. ('limits', 'cursor',
            'stream')
        page_size : :obj:`int`
            Number of objects to be returned in each page. Page size can range
            between 1 and 1000 objects.
        page : :obj:`int`
            An integer for the wanted page of results. Used only with
            `pagination_type` set as `limits`.
        next : :obj:`str`
            An alphanumeric string bookmark to indicate where to start for the
            next page. Used only with `pagination_type` set as `cursor`.
        previous : :obj:`str`
            An alphanumeric string bookmark to indicate where to end for the
            previous page. Used only with `pagination_type` set as `cursor`.
        direction : :obj:`Literal['asc', 'desc']`
            Sorting order according to the `sort_by` parameter. ('asc', 'desc')
        sort_by : :obj:`Sequence[str]`
            Sort the results by one or more enumerators.
        data: requests.LastParametersResourcesGet, optional
        **kwargs:
            Extra parameters for requests.LastParametersResourcesGet
              - get_last_parameters_resources: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/resources/last/get",
            {},
            {
                "pagination_type": pagination_type,
                "page_size": page_size,
                "page": page,
                "next": next,
                "previous": previous,
                "direction": direction,
                "sort_by": sort_by,
            },
            {},
            {},
            data,
            "requests.LastParametersResourcesGet",
            False,
            {
                "200": responses.LastParametersResourcesGetPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[KList[responses.ParameterValueItem], responses.LastParametersResourcesGetPaginatedResponseCursor],
                cls.fetch(_client, "/api/v4/parameters/resources/last/get", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def list_resource_parameters(
        cls,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.ResourceParametersList, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[responses.ParameterValueHistorianItem], responses.ResourceParametersListPaginatedResponseCursor]:
        """
        Returns a list of Parameters and all values for each Resource. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``listResourceParameters``: ``POST`` ``/api/v4/parameters/resources/list``

        Parameters
        ----------
        pagination_type : :obj:`Literal['limits', 'cursor', 'stream']`
            Method of pagination to use for return results where `total_items` is
            greater than `page_size`. `cursor` and `limits` will return one `page`
            of results, `stream` will return all results. ('limits', 'cursor',
            'stream')
        page_size : :obj:`int`
            Number of objects to be returned in each page. Page size can range
            between 1 and 1000 objects.
        page : :obj:`int`
            An integer for the wanted page of results. Used only with
            `pagination_type` set as `limits`.
        next : :obj:`str`
            An alphanumeric string bookmark to indicate where to start for the
            next page. Used only with `pagination_type` set as `cursor`.
        previous : :obj:`str`
            An alphanumeric string bookmark to indicate where to end for the
            previous page. Used only with `pagination_type` set as `cursor`.
        direction : :obj:`Literal['asc', 'desc']`
            Sorting order according to the `sort_by` parameter. ('asc', 'desc')
        sort_by : :obj:`Sequence[str]`
            Sort the results by one or more enumerators.
        data: requests.ResourceParametersList, optional
        **kwargs:
            Extra parameters for requests.ResourceParametersList
              - list_resource_parameters: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/resources/list",
            {},
            {
                "pagination_type": pagination_type,
                "page_size": page_size,
                "page": page,
                "next": next,
                "previous": previous,
                "direction": direction,
                "sort_by": sort_by,
            },
            {},
            {},
            data,
            "requests.ResourceParametersList",
            False,
            {
                "200": responses.ResourceParametersListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[
                    KList[responses.ParameterValueHistorianItem],
                    responses.ResourceParametersListPaginatedResponseCursor,
                ],
                cls.fetch(_client, "/api/v4/parameters/resources/list", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def create_parameters_schedule(
        cls,
        data: Optional[Union[requests.ParametersScheduleCreate, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.ParametersScheduleCreate:
        """
        Create a new schedule to apply parameters to an application.

        Schedules are sets of application parameter values that are applied to a
        group of assets at a given time.

        Optionally, those values can be reverted to the desired value. When doing
        so, parameter values are defined for each asset individually, and the
        assets and parameters must match the original schedule. For example, if 2
        parameters were changed for 2 assets and a revert operation is requested,
        then the revert parameters must have 2 assets and 2 parameters for each
        asset.

        The schedule must be created in the future and, if a revert operation is
        requested, the revert date must be after the scheduled date.

        Upon creation, the current values of the parameters are stored in the
        `original_resource_parameters` field.

        **Permission Required:** `kelvin.permission.parameter.update`.

        ``createParametersSchedule``: ``POST`` ``/api/v4/parameters/schedule/create``

        Parameters
        ----------
        data: requests.ParametersScheduleCreate, optional
        **kwargs:
            Extra parameters for requests.ParametersScheduleCreate
              - create_parameters_schedule: str

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/schedule/create",
            {},
            {},
            {},
            {},
            data,
            "requests.ParametersScheduleCreate",
            False,
            {
                "201": responses.ParametersScheduleCreate,
                "400": response.Error,
                "401": response.Error,
                "409": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def list_parameters_schedule(
        cls,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.ParametersScheduleList, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[responses.ParametersScheduleGet], responses.ParametersScheduleListPaginatedResponseCursor]:
        """
        List schedules based on filters.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``listParametersSchedule``: ``POST`` ``/api/v4/parameters/schedule/list``

        Parameters
        ----------
        pagination_type : :obj:`Literal['limits', 'cursor', 'stream']`
            Method of pagination to use for return results where `total_items` is
            greater than `page_size`. `cursor` and `limits` will return one `page`
            of results, `stream` will return all results. ('limits', 'cursor',
            'stream')
        page_size : :obj:`int`
            Number of objects to be returned in each page. Page size can range
            between 1 and 1000 objects.
        page : :obj:`int`
            An integer for the wanted page of results. Used only with
            `pagination_type` set as `limits`.
        next : :obj:`str`
            An alphanumeric string bookmark to indicate where to start for the
            next page. Used only with `pagination_type` set as `cursor`.
        previous : :obj:`str`
            An alphanumeric string bookmark to indicate where to end for the
            previous page. Used only with `pagination_type` set as `cursor`.
        direction : :obj:`Literal['asc', 'desc']`
            Sorting order according to the `sort_by` parameter. ('asc', 'desc')
        sort_by : :obj:`Sequence[str]`
            Sort the results by one or more enumerators.
        data: requests.ParametersScheduleList, optional
        **kwargs:
            Extra parameters for requests.ParametersScheduleList
              - list_parameters_schedule: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/schedule/list",
            {},
            {
                "pagination_type": pagination_type,
                "page_size": page_size,
                "page": page,
                "next": next,
                "previous": previous,
                "direction": direction,
                "sort_by": sort_by,
            },
            {},
            {},
            data,
            "requests.ParametersScheduleList",
            False,
            {
                "200": responses.ParametersScheduleListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[KList[responses.ParametersScheduleGet], responses.ParametersScheduleListPaginatedResponseCursor],
                cls.fetch(_client, "/api/v4/parameters/schedule/list", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def apply_parameters_schedule(
        cls,
        schedule_id: str,
        data: Optional[Union[requests.ParametersScheduleApply, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Apply the scheduled or reverted parameters of a specific schedule.

        There are 2 types of the "apply" action:

        - `schedule`: Applies the scheduled parameters if the schedule is in the
        `scheduled` state.
        - `schedule-revert`: Applies the revert parameters if the schedule is in the
        `scheduled-revert` state.

        If the schedule is not in the supported state for the selected type, the
        API will return an error.

        Errors encountered when calling this API will not affect the schedule
        state.

        **Permission Required:** `kelvin.permission.parameter.update`.

        ``applyParametersSchedule``: ``POST`` ``/api/v4/parameters/schedule/{schedule_id}/apply``

        Parameters
        ----------
        schedule_id : :obj:`str`, optional
            Schedule ID
        data: requests.ParametersScheduleApply, optional
        **kwargs:
            Extra parameters for requests.ParametersScheduleApply
              - apply_parameters_schedule: dict

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/schedule/{schedule_id}/apply",
            {"schedule_id": schedule_id},
            {},
            {},
            {},
            data,
            "requests.ParametersScheduleApply",
            False,
            {"200": None, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def delete_parameters_schedule(cls, schedule_id: str, _dry_run: bool = False, _client: Any = None) -> None:
        """
        Delete a specific schedule.

        **Permission Required:** `kelvin.permission.parameter.delete`.

        ``deleteParametersSchedule``: ``POST`` ``/api/v4/parameters/schedule/{schedule_id}/delete``

        Parameters
        ----------
        schedule_id : :obj:`str`, optional
            Schedule ID

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/schedule/{schedule_id}/delete",
            {"schedule_id": schedule_id},
            {},
            {},
            {},
            None,
            None,
            False,
            {"200": None, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
        )
        return result

    @classmethod
    def get_parameters_schedule(
        cls, schedule_id: str, _dry_run: bool = False, _client: Any = None
    ) -> responses.ParametersScheduleGet:
        """
        Get a specific schedule.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``getParametersSchedule``: ``GET`` ``/api/v4/parameters/schedule/{schedule_id}/get``

        Parameters
        ----------
        schedule_id : :obj:`str`, optional
            Schedule ID

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/parameters/schedule/{schedule_id}/get",
            {"schedule_id": schedule_id},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.ParametersScheduleGet,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def get_parameters_values(
        cls,
        data: Optional[Union[requests.ParametersValuesGet, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.ParametersValuesGet:
        """
        Returns a list of all unique values for each Parameter. Default values will not be shown. If the App is not specified, then the response will be grouped by App Name.

        **Permission Required:** `kelvin.permission.parameter.read`.

        ``getParametersValues``: ``POST`` ``/api/v4/parameters/values/get``

        Parameters
        ----------
        data: requests.ParametersValuesGet, optional
        **kwargs:
            Extra parameters for requests.ParametersValuesGet
              - get_parameters_values: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/parameters/values/get",
            {},
            {},
            {},
            {},
            data,
            "requests.ParametersValuesGet",
            False,
            {"200": responses.ParametersValuesGet, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result
