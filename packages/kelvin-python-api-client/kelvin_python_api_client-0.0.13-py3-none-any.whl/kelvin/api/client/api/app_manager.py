"""
Kelvin API Client.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, Union, cast

from typing_extensions import Literal

from kelvin.api.client.api_service_model import ApiServiceModel
from kelvin.api.client.data_model import KList

from ..model import requests, response, responses, type


class AppManager(ApiServiceModel):
    @classmethod
    def get_app_manager_app(
        cls, app_name: str, _dry_run: bool = False, _client: Any = None
    ) -> responses.AppManagerAppGet:
        """
        Retrieve the parameters of an Application.

        **Permission Required:** `kelvin.permission.appmanager.read`.

        ``getAppManagerApp``: ``GET`` ``/api/v4/app-manager/app/{app_name}/get``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            A filter on the list based on the Application key `name`. The filter
            is on the full name only. All strings in the array are treated as
            `OR`. Can only contain lowercase alphanumeric characters and `.`, `_`
            or `-` characters.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/app-manager/app/{app_name}/get",
            {"app_name": app_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {"200": responses.AppManagerAppGet, "400": response.Error, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
        )
        return result

    @classmethod
    def get_app_manager_app_planner_rules(
        cls, app_name: str, _dry_run: bool = False, _client: Any = None
    ) -> responses.AppManagerAppPlannerRulesGet:
        """
        Return the Planner Rules for the specified Application.

        ``getAppManagerAppPlannerRules``: ``GET`` ``/api/v4/app-manager/app/{app_name}/planner-rules/get``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to deploy.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/app-manager/app/{app_name}/planner-rules/get",
            {"app_name": app_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {"200": responses.AppManagerAppPlannerRulesGet, "401": response.Error, "404": response.Error},
            False,
            _dry_run,
        )
        return result

    @classmethod
    def update_app_manager_app_planner_rules(
        cls,
        app_name: str,
        data: Optional[Union[requests.AppManagerAppPlannerRulesUpdate, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.AppManagerAppPlannerRulesUpdate:
        """
        Updates the Planner Rules for the specified Application. The object in the payload is applied as a whole, not merged with the existing object.

        For example if the key `cluster` is currently set, updating with a payload without that key will set it to an empty string.

        ``updateAppManagerAppPlannerRules``: ``POST`` ``/api/v4/app-manager/app/{app_name}/planner-rules/update``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to deploy.
        data: requests.AppManagerAppPlannerRulesUpdate, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppPlannerRulesUpdate
              - update_app_manager_app_planner_rules: str

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/planner-rules/update",
            {"app_name": app_name},
            {},
            {},
            {},
            data,
            "requests.AppManagerAppPlannerRulesUpdate",
            False,
            {
                "201": responses.AppManagerAppPlannerRulesUpdate,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def list_app_manager_app_resources(
        cls,
        app_name: str,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.AppManagerAppResourcesList, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[responses.AppManagerResourceContext], responses.AppManagerAppResourcesListPaginatedResponseCursor]:
        """
        Returns a list of Assets and associated information running on an Application. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.appmanager.read`.

        ``listAppManagerAppResources``: ``POST`` ``/api/v4/app-manager/app/{app_name}/resources/list``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            A filter on the list based on the Application key `name`. The filter
            is on the full name only. All strings in the array are treated as
            `OR`. Can only contain lowercase alphanumeric characters and `.`, `_`
            or `-` characters.
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
        data: requests.AppManagerAppResourcesList, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppResourcesList
              - list_app_manager_app_resources: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/resources/list",
            {"app_name": app_name},
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
            "requests.AppManagerAppResourcesList",
            False,
            {
                "200": responses.AppManagerAppResourcesListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[
                    KList[responses.AppManagerResourceContext],
                    responses.AppManagerAppResourcesListPaginatedResponseCursor,
                ],
                cls.fetch(_client, "/api/v4/app-manager/app/{app_name}/resources/list", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def get_app_manager_app_version_data_mapping(
        cls,
        app_name: str,
        version: str,
        data: Optional[Union[requests.AppManagerAppVersionDataMappingGet, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.AppManagerAppVersionDataMappingGet:
        """
        Retrieve a list of all the Input and Output mappings between an Application and the Assets and Data Streams.

        **Permission Required:** `kelvin.permission.appmanager.read`.

        ``getAppManagerAppVersionDataMapping``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/data-mapping``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            A filter on the list based on the Application key `name`. The filter
            is on the full name only. All strings in the array are treated as
            `OR`. Can only contain lowercase alphanumeric characters and `.`, `_`
            or `-` characters.
        version : :obj:`str`, optional
            Version of Application to check for Assets.
        data: requests.AppManagerAppVersionDataMappingGet, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionDataMappingGet
              - get_app_manager_app_version_data_mapping: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/data-mapping",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            data,
            "requests.AppManagerAppVersionDataMappingGet",
            False,
            {"200": responses.AppManagerAppVersionDataMappingGet, "400": response.Error, "401": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def deploy_app_manager_app_version(
        cls,
        app_name: str,
        version: str,
        dry_run: Optional[bool] = None,
        data: Optional[Union[requests.AppManagerAppVersionDeploy, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.AppManagerAppVersionDeploy:
        """
        Deploy the version of an Application to an edge or cloud Cluster.

        The request can contain which Resources to deploy the Application to,
        Parameters, Deployment Overrides, and Planner Rules. Besides Resources, all
        other fields are optional. Depending on the field, their values will be
        defined by:

        - Resource Parameters: Loaded from the Parameters API. If the parameter is
        set for that resource, it will be used. If not and a previous version has
        the parameter set, it will inherit that value. Otherwise it will not be
        set.
        - Deployment Overrides: Loaded from the Install Manifest, which in turn is
        filled by the app.yaml.
        - Planner Rules: Loaded from the Application's configuration. In the case
        of the Data Stream Map, if it is not provided and a default is not set, it
        will fallback to using the same name of the inputs/outputs as the data
        streams.

        **Permission Required:** `kelvin.permission.appmanager.create`.

        ``deployAppManagerAppVersion``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/deploy``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to deploy.
        version : :obj:`str`, optional
            Version of Application to deploy.
        dry_run : :obj:`bool`
            Executes a simulated run when set to true, providing feedback without
            altering server data.
        data: requests.AppManagerAppVersionDeploy, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionDeploy
              - deploy_app_manager_app_version: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/deploy",
            {"app_name": app_name, "version": version},
            {"dry_run": dry_run},
            {},
            {},
            data,
            "requests.AppManagerAppVersionDeploy",
            False,
            {
                "201": responses.AppManagerAppVersionDeploy,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def quickdeploy_app_manager_app_version(
        cls,
        app_name: str,
        version: str,
        dry_run: Optional[bool] = None,
        data: Optional[Union[requests.AppManagerAppVersionQuickdeploy, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.AppManagerAppVersionQuickdeploy:
        """
        Deploy an Application for the selected resources using default
        configurations.

        It is a simplified version of the deploy operation in which only the
        resources can be specified and the workloads are reused. Additionally, it
        requires a different permission.

        **Permission Required:** `kelvin.permission.appmanager.quick_deploy`.

        ``quickdeployAppManagerAppVersion``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/quick-deploy``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to deploy.
        version : :obj:`str`, optional
            Version of Application to deploy.
        dry_run : :obj:`bool`
            Executes a simulated run when set to true, providing feedback without
            altering server data.
        data: requests.AppManagerAppVersionQuickdeploy, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionQuickdeploy
              - quickdeploy_app_manager_app_version: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/quick-deploy",
            {"app_name": app_name, "version": version},
            {"dry_run": dry_run},
            {},
            {},
            data,
            "requests.AppManagerAppVersionQuickdeploy",
            False,
            {
                "201": responses.AppManagerAppVersionQuickdeploy,
                "207": responses.AppManagerAppVersionQuickdeploy,
                "400": response.Error,
                "401": response.Error,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def start_app_manager_app_version(
        cls,
        app_name: str,
        version: str,
        data: Optional[Union[requests.AppManagerAppVersionStart, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Start running the Asset(s) associated with the Application Version. This API request allows batch starting of multiple Assets for a given Application.

        **Permission Required:** `kelvin.permission.appmanager.update`.

        ``startAppManagerAppVersion``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/start``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to associate with Assets (resources) to perform
            the required actions.
        version : :obj:`str`, optional
            Version of Application.
        data: requests.AppManagerAppVersionStart, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionStart
              - start_app_manager_app_version: str

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/start",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            data,
            "requests.AppManagerAppVersionStart",
            False,
            {"200": None, "207": None, "400": response.Error, "401": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def stop_app_manager_app_version(
        cls,
        app_name: str,
        version: str,
        data: Optional[Union[requests.AppManagerAppVersionStop, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Stop running the Asset(s) associated with the Application Version. This API request allows batch starting of multiple Assets for a given Application.

        **Permission Required:** `kelvin.permission.appmanager.update`.

        ``stopAppManagerAppVersion``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/stop``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to associate with Assets (resources) to perform
            the required actions.
        version : :obj:`str`, optional
            Version of Application.
        data: requests.AppManagerAppVersionStop, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionStop
              - stop_app_manager_app_version: str

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/stop",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            data,
            "requests.AppManagerAppVersionStop",
            False,
            {"200": None, "207": None, "400": response.Error, "401": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def undeploy_app_manager_app_version(
        cls,
        app_name: str,
        version: str,
        data: Optional[Union[requests.AppManagerAppVersionUndeploy, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Undeploy (remove) an Application from an edge or cloud Cluster. This will only remove the specified version.

        **Permission Required:** `kelvin.permission.appmanager.delete`.

        ``undeployAppManagerAppVersion``: ``POST`` ``/api/v4/app-manager/app/{app_name}/v/{version}/undeploy``

        Parameters
        ----------
        app_name : :obj:`str`, optional
            Application key `name` to associate with Assets (resources) to perform
            the required actions.
        version : :obj:`str`, optional
            Version of Application.
        data: requests.AppManagerAppVersionUndeploy, optional
        **kwargs:
            Extra parameters for requests.AppManagerAppVersionUndeploy
              - undeploy_app_manager_app_version: str

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/app/{app_name}/v/{version}/undeploy",
            {"app_name": app_name, "version": version},
            {},
            {},
            {},
            data,
            "requests.AppManagerAppVersionUndeploy",
            False,
            {"200": None, "207": None, "400": response.Error, "401": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def list_app_manager(
        cls,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Sequence[str]] = None,
        data: Optional[Union[requests.AppManagerList, Mapping[str, Any]]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> Union[KList[type.AppManagerApp], responses.AppManagerListPaginatedResponseCursor]:
        """
        Returns a list of Application objects. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.appmanager.read`.

        ``listAppManager``: ``POST`` ``/api/v4/app-manager/list``

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
        data: requests.AppManagerList, optional
        **kwargs:
            Extra parameters for requests.AppManagerList
              - list_app_manager: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/app-manager/list",
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
            "requests.AppManagerList",
            False,
            {"200": responses.AppManagerListPaginatedResponseCursor, "400": response.Error, "401": response.Error},
            False,
            _dry_run,
            kwargs,
        )
        return (
            cast(
                Union[KList[type.AppManagerApp], responses.AppManagerListPaginatedResponseCursor],
                cls.fetch(_client, "/api/v4/app-manager/list", result, "POST", data),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def get_app_manager_resource(
        cls,
        resource_krn: str,
        pagination_type: Optional[Literal["limits", "cursor", "stream"]] = None,
        page_size: Optional[int] = 10000,
        page: Optional[int] = None,
        next: Optional[str] = None,
        previous: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        sort_by: Optional[Literal["name", "title", "description", "version"]] = None,
        fetch: bool = True,
        _dry_run: bool = False,
        _client: Any = None,
    ) -> Union[KList[type.AppManagerAppVersionSummary], responses.AppManagerResourceGetPaginatedResponseCursor]:
        """
        Returns a list of all Applications associated with an Asset (`resource`).

        **Permission Required:** `kelvin.permission.appmanager.read`.

        ``getAppManagerResource``: ``GET`` ``/api/v4/app-manager/resource/{resource_krn}/get``

        Parameters
        ----------
        resource_krn : :obj:`str`, optional
            The Asset (`resource`) entered as a KRN value.
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
        sort_by : :obj:`Literal['name', 'title', 'description', 'version']`
            Sort the results by one or more enumerators. ('name', 'title',
            'description', 'version')

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/app-manager/resource/{resource_krn}/get",
            {"resource_krn": resource_krn},
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
            None,
            None,
            False,
            {
                "200": responses.AppManagerResourceGetPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
            },
            False,
            _dry_run,
        )
        return (
            cast(
                Union[KList[type.AppManagerAppVersionSummary], responses.AppManagerResourceGetPaginatedResponseCursor],
                cls.fetch(_client, "/api/v4/app-manager/resource/{resource_krn}/get", result, "GET"),
            )
            if fetch and not _dry_run
            else result
        )
