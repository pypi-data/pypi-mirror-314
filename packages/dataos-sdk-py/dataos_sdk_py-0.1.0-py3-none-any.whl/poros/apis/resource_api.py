from __future__ import absolute_import

from uplink import *
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code


class ResourceApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v1/resources/depot/{name}")
    def fetch_depot(self, name: str):
        """
        Fetches a depot resource by name.

        Parameters:
            name (str): The name of the depot resource specified in the URL.

        Returns:
            json: The JSON response as a dictionary.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/service/{name}")
    def fetch_service(self, workspace: str, name: str):
        """
        Fetches service details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the service from (sent as a path parameter).
            name (str): The name of the service to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing service details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/cluster/{name}")
    def fetch_cluster(self, workspace: str, name: str):
        """
        Fetches cluster details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the cluster from (sent as a path parameter).
            name (str): The name of the cluster to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing cluster details.
        """

        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/secret/{name}")
    def fetch_secret(self, workspace: str, name: str):
        """
        Fetches secret details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the secret from (sent as a path parameter).
            name (str): The name of the secret to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing secret details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/database/{name}")
    def fetch_database(self, workspace: str, name: str):
        """
        Fetches database details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the database from (sent as a path parameter).
            name (str): The name of the database to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing database details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/workflow/{name}")
    def fetch_workflow(self, workspace: str, name: str):
        """
        Fetches workflow details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the workflow from (sent as a path parameter).
            name (str): The name of the workflow to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing workflow details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/workflow")
    def fetch_workflows(self, workspace: str):
        """
        Fetches workflow details by workspace and name.

        Parameters:
            workspace (str): The workspace to retrieve the workflow from (sent as a path parameter).

        Returns:
            json array: The JSON response as a dictionary containing list of workflow details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}")
    def fetch_workspace(self, workspace):
        """
        Fetches workspace details by workspace name.

        Parameters:
            workspace (str): The name of the workspace to fetch (sent as a path parameter).

        Returns:
            json: The JSON response as a dictionary containing workspace details.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/workspaces/{workspace}/resources/{type}/{name}")
    def fetch_resource(self, workspace: str, type: str, name: str):
        """
        Fetches resource details by workspace, type, and name.

        Parameters:
            workspace (str): The workspace to retrieve the resource from (sent as a path parameter).
            type (str): The type of the resource (e.g., "service", "cluster", "secret", etc., sent as a path parameter).
            name (str): The name of the resource to fetch (sent as a path parameter).

        Returns:
            uplink.json: The JSON response as a dictionary containing resource details.
        """
        pass
