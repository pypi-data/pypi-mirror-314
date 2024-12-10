from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from stack_service.apis.stack_context_api import StackContextApi


class StackServiceClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "StackServiceClient"

    def build(self):
        """
        Build the StackServiceClient instance.

        Returns:
            StackServiceClient: An instance of StackServiceClient with the configured settings.
        """
        return StackServiceClient(self.base_url, self.apikey, self.get_http_client())


class StackServiceClient:
    def __init__(self, base_url, apikey, client = None):
        """
        Initialize the StackServiceClient.

        This class provides a client to interact with an API related to stack services.

        Parameters:
            base_url (str): The base URL of the Stack Service API.
            apikey (str): The API key for authentication with the Stack Service API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            open_lineage_api (OpenLineageApi): An instance of OpenLineageApi for interacting with the OpenLineage API endpoints.
        """
        self.client = client
        self.base_url = base_url
        self.apikey = apikey

        base_url = normalize_base_url(base_url)
        self.stack_context_api = StackContextApi(base_url, self.apikey, client=self.client)
