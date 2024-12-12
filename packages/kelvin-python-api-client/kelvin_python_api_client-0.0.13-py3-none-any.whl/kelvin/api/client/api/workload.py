"""
Kelvin API Client.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Optional, Sequence, Union, cast

from typing_extensions import Literal

from kelvin.api.client.api_service_model import ApiServiceModel
from kelvin.api.client.data_model import KList

from ..model import requests, response, responses


class Workload(ApiServiceModel):
    @classmethod
    def apply_workload(
        cls,
        data: Optional[Union[requests.WorkloadApply, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Initiate final deploy action for the downloaded Workloads. Only valid for Workloads that were previously deployed with the keys `staged` set to true and `instantly_apply` set to false.

        **Permission Required:** `kelvin.permission.workload.update`.

        ``applyWorkload``: ``POST`` ``/api/v4/workloads/apply``

        Parameters
        ----------
        data: requests.WorkloadApply, optional
        **kwargs:
            Extra parameters for requests.WorkloadApply
              - apply_workload: dict

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/workloads/apply",
            {},
            {},
            {},
            {},
            data,
            "requests.WorkloadApply",
            False,
            {
                "200": None,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "406": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def deploy_workload(
        cls,
        data: Optional[Union[requests.WorkloadDeploy, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.WorkloadDeploy:
        """
        Deploy an App from the App Registry as a Workload to a Cluster/Node.

        **Permission Required:** `kelvin.permission.workload.update`.

        ``deployWorkload``: ``POST`` ``/api/v4/workloads/deploy``

        Parameters
        ----------
        data: requests.WorkloadDeploy, optional
        **kwargs:
            Extra parameters for requests.WorkloadDeploy
              - deploy_workload: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/workloads/deploy",
            {},
            {},
            {},
            {},
            data,
            "requests.WorkloadDeploy",
            False,
            {
                "201": responses.WorkloadDeploy,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def list_workloads(
        cls,
        search: Optional[Sequence[str]] = None,
        app_name: Optional[Sequence[str]] = None,
        app_version: Optional[Sequence[str]] = None,
        acp_name: Optional[Sequence[str]] = None,
        cluster_name: Optional[Sequence[str]] = None,
        node_name: Optional[Sequence[str]] = None,
        workload_name: Optional[Sequence[str]] = None,
        enabled: Optional[bool] = None,
        asset_name: Optional[str] = None,
        staged: Optional[bool] = None,
        download_statuses: Optional[Sequence[str]] = None,
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
    ) -> Union[KList[responses.WorkloadItem], responses.WorkloadsListPaginatedResponseCursor]:
        """
        Returns a list of Workload objects. The list can be optionally filtered and sorted on the server before being returned.

        **Permission Required:** `kelvin.permission.workload.read`.

        ``listWorkloads``: ``GET`` ``/api/v4/workloads/list``

        Parameters
        ----------
        search : :obj:`Sequence[str]`
            Search and filter on the list based on the keys `name`, `title`
            (Display Name), `app_name`, `cluster_name` and `node_name`. All
            strings in the array are treated as `OR`. The search is case
            insensitive and will find partial matches as well.
        app_name : :obj:`Sequence[str]`
            A filter on the list based on the key `app_name`. The filter is on the
            full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters.
        app_version : :obj:`Sequence[str]`
            A filter on the list based on the key `app_version`. The filter is on
            the full value only. The string can only contain lowercase
            alphanumeric characters and `.`, `_` or `-` characters.
        acp_name : :obj:`Sequence[str]`
            [`Deprecated`] A filter on the list based on the key `acp_name`. The
            filter is on the full name only. The string can only contain lowercase
            alphanumeric characters and `.`, `_` or `-` characters.
        cluster_name : :obj:`Sequence[str]`
            A filter on the list based on the key `cluster_name`. The filter is on
            the full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters. If set, it will override
            acp_name
        node_name : :obj:`Sequence[str]`
            A filter on the list based on the key `node_name`. The filter is on
            the full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters.
        workload_name : :obj:`Sequence[str]`
            A filter on the list based on the key `name`. The filter is on the
            full name only. The string can only contain lowercase alphanumeric
            characters and `.`, `_` or `-` characters.
        enabled : :obj:`bool`
            A filter on the list based on the key `status` (start/stop function in
            Kelvin UI) of the Workloads.
        asset_name : :obj:`str`
            A filter on the list based on Asset `name` associated with the
            Workload. The filter is on the full name only. The string can only
            contain lowercase alphanumeric characters and `.`, `_` or `-`
            characters.
        staged : :obj:`bool`
            A filter on the key staged. Using true will only show staged
            workloads, false will show all workloads.
        download_statuses : :obj:`Sequence[str]`
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

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/list",
            {},
            {
                "search": search,
                "app_name": app_name,
                "app_version": app_version,
                "acp_name": acp_name,
                "cluster_name": cluster_name,
                "node_name": node_name,
                "workload_name": workload_name,
                "enabled": enabled,
                "asset_name": asset_name,
                "staged": staged,
                "download_statuses": download_statuses,
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
                "200": responses.WorkloadsListPaginatedResponseCursor,
                "400": response.Error,
                "401": response.Error,
                "500": response.Error,
            },
            False,
            _dry_run,
        )
        return (
            cast(
                Union[KList[responses.WorkloadItem], responses.WorkloadsListPaginatedResponseCursor],
                cls.fetch(_client, "/api/v4/workloads/list", result, "GET"),
            )
            if fetch and not _dry_run
            else result
        )

    @classmethod
    def get_workload_configuration(
        cls, workload_name: str, _dry_run: bool = False, _client: Any = None
    ) -> responses.WorkloadConfigurationGet:
        """
        Retrieve the configuration of a Workload.

        **Permission Required:** `kelvin.permission.workload.read`.

        ``getWorkloadConfiguration``: ``GET`` ``/api/v4/workloads/{workload_name}/configurations/get``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/configurations/get",
            {"workload_name": workload_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.WorkloadConfigurationGet,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def update_workload_configuration(
        cls,
        workload_name: str,
        data: Optional[Union[requests.WorkloadConfigurationUpdate, Mapping[str, Any]]] = None,
        _dry_run: bool = False,
        _client: Any = None,
        **kwargs: Any,
    ) -> responses.WorkloadConfigurationUpdate:
        """
        Update the configuration of a Workload.

        **Permission Required:** `kelvin.permission.workload.update`

        **`WARNING!!`: Sending an empty configuration object will remove all configurations**.

        ``updateWorkloadConfiguration``: ``POST`` ``/api/v4/workloads/{workload_name}/configurations/update``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.
        data: requests.WorkloadConfigurationUpdate, optional
        **kwargs:
            Extra parameters for requests.WorkloadConfigurationUpdate
              - update_workload_configuration: dict

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/workloads/{workload_name}/configurations/update",
            {"workload_name": workload_name},
            {},
            {},
            {},
            data,
            "requests.WorkloadConfigurationUpdate",
            False,
            {
                "200": responses.WorkloadConfigurationUpdate,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
            kwargs,
        )
        return result

    @classmethod
    def download_workload(
        cls, workload_name: str, address: Optional[bool] = None, _dry_run: bool = False, _client: Any = None
    ) -> str:
        """
        Download the Workload package file for offline installation on the Edge System. The system automatically generates the file for download if the package is not already available.

        **Permission Required:** `kelvin.permission.workload.read`.

        ``downloadWorkload``: ``GET`` ``/api/v4/workloads/{workload_name}/download``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.
        address : :obj:`bool`
            If true, the endpoint will return a direct URL to the workload package
            file.

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/download",
            {"workload_name": workload_name},
            {"address": address},
            {},
            {},
            None,
            None,
            False,
            {
                "200": str,
                "202": None,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "412": response.Error,
                "500": response.Error,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def get_workload(cls, workload_name: str, _dry_run: bool = False, _client: Any = None) -> responses.WorkloadGet:
        """
        Retrieve the parameters of a Workload.

        **Permission Required:** `kelvin.permission.workload.read`.

        ``getWorkload``: ``GET`` ``/api/v4/workloads/{workload_name}/get``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/get",
            {"workload_name": workload_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.WorkloadGet,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "500": response.Error,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def get_workload_logs(
        cls,
        workload_name: str,
        tail_lines: Optional[int] = None,
        since_time: Optional[datetime] = None,
        _dry_run: bool = False,
        _client: Any = None,
    ) -> responses.WorkloadLogsGet:
        """
        Get Workload Logs

        **Permission Required:** `kelvin.permission.workload.read`.

        ``getWorkloadLogs``: ``GET`` ``/api/v4/workloads/{workload_name}/logs/get``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.
        tail_lines : :obj:`int`
            Specify the number of the most recent log lines to retrieve, counting
            backwards from the latest entry.
        since_time : :obj:`datetime`
            UTC time of the starting point for log retrieval, formatted in RFC
            3339.

        """

        from ..model import response, responses

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/logs/get",
            {"workload_name": workload_name},
            {"tail_lines": tail_lines, "since_time": since_time},
            {},
            {},
            None,
            None,
            False,
            {
                "200": responses.WorkloadLogsGet,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def start_workload(cls, workload_name: str, _dry_run: bool = False, _client: Any = None) -> None:
        """
        Start running the Workload.

        **Permission Required:** `kelvin.permission.workload.update`.

        ``startWorkload``: ``GET`` ``/api/v4/workloads/{workload_name}/start``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/start",
            {"workload_name": workload_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": None,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def stop_workload(cls, workload_name: str, _dry_run: bool = False, _client: Any = None) -> None:
        """
        Stop running the Workload.

        **Permission Required:** `kelvin.permission.workload.update`.

        ``stopWorkload``: ``GET`` ``/api/v4/workloads/{workload_name}/stop``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "get",
            "/api/v4/workloads/{workload_name}/stop",
            {"workload_name": workload_name},
            {},
            {},
            {},
            None,
            None,
            False,
            {
                "200": None,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "409": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
        )
        return result

    @classmethod
    def undeploy_workload(
        cls, workload_name: str, staged: Optional[bool] = None, _dry_run: bool = False, _client: Any = None
    ) -> None:
        """
        Undeploy Workload from the Edge System.

        **Permission Required:** `kelvin.permission.workload.delete`.

        ``undeployWorkload``: ``POST`` ``/api/v4/workloads/{workload_name}/undeploy``

        Parameters
        ----------
        workload_name : :obj:`str`, optional
            Unique identifier `name` of the Workload.
        staged : :obj:`bool`
            If true, the endpoint only undeploys the staged workload, if any.

        """

        from ..model import response

        result = cls._make_request(
            _client,
            "post",
            "/api/v4/workloads/{workload_name}/undeploy",
            {"workload_name": workload_name},
            {"staged": staged},
            {},
            {},
            None,
            None,
            False,
            {
                "200": None,
                "400": response.Error,
                "401": response.Error,
                "404": response.Error,
                "500": response.Error,
                "501": None,
            },
            False,
            _dry_run,
        )
        return result
