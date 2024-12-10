from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from poros.apis.resource_api import ResourceApi


class PorosClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "PorosClient"

    def build(self):
        """
        Build the PorosClient instance.

        Returns:
            PorosClient: An instance of PorosClient with the configured settings.
        """
        return PorosClient(self.base_url, self.apikey, self.get_http_client())


class PorosClient:
    def __init__(self, base_url, apikey, client=None):
        """
        Initialize the PorosClient.

        This class provides a client to interact with various API endpoints related to Poros.

        Parameters:
            base_url (str): The base URL of the Poros API.
            apikey (str): The API key for authentication with the Poros API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            resource_api (ResourceApi): An instance of ResourceApi for interacting with the Resource API endpoints.
        """
        self.client = client
        self.base_url = base_url
        self.apikey = apikey

        base_url = normalize_base_url(base_url)
        self.resource_api = ResourceApi(base_url, self.apikey, client=self.client)
