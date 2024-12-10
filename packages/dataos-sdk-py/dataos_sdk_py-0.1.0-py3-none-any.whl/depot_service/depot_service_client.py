from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from depot_service.apis.dataset_api import DatasetApi
from depot_service.apis.depot_api import DepotApi
from depot_service.apis.resolver_api import ResolveApi
from depot_service.apis.secret_api import SecretApi

import requests


class DepotServiceClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "DepotServiceClient"

    def build(self):
        """
        Build the DepotServiceClient instance.

        Returns:
            DepotServiceClient: An instance of DepotServiceClient with the configured settings.
        """
        return DepotServiceClient(self.base_url, self.apikey, self.get_http_client())


class DepotServiceClient:
    def __init__(self, base_url, apikey, client=None):
        """
        Initialize the DepotServiceClient.

        This class provides a client to interact with various API endpoints related to depots.

        Parameters:
            base_url (str): The base URL of the Depot Service API.
            apikey (str): The API key for authentication with the Depot Service API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            resolve_api (ResolveApi): An instance of ResolveApi for interacting with the Resolve API endpoints.
            dataset_api (DatasetApi): An instance of DatasetApi for interacting with the Dataset API endpoints.
            secret_api (SecretApi): An instance of SecretApi for interacting with the Secret API endpoints.
            depot_api (DepotApi): An instance of DepotApi for interacting with the Depot API endpoints.
        """
        self.client = client
        self.base_url = base_url
        self.apikey = apikey
        base_url = normalize_base_url(self.base_url)
        self.resolve_api = ResolveApi(base_url, self.apikey, client=self.client)
        self.dataset_api = DatasetApi(base_url, self.apikey, client=self.client)
        self.secret_api = SecretApi(base_url, self.apikey, client=self.client)
        self.depot_api = DepotApi(base_url, self.apikey, client=self.client)
