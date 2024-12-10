from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from gateway.apis.data_policy_api import DataPolicyApi


class GatewayClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "GatewayClient"

    def build(self):
        """
        Build the GatewayClient instance.

        Returns:
            GatewayClient: An instance of GatewayClient with the configured settings.
        """
        return GatewayClient(self.base_url, self.apikey, self.get_http_client())

class GatewayClient:
    def __init__(self, base_url, apikey, client = None):
        """
        Initialize the GatewayClient.

        This class provides a client to interact with various API endpoints related to the Gateway.

        Parameters:
            base_url (str): The base URL of the Gateway API.
            apikey (str): The API key for authentication with the Gateway API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            data_policy_api (DataPolicyApi): An instance of DataPolicyApi for interacting with the Data Policy API endpoints.
        """
        self.client = client
        self.base_url = base_url
        self.apikey = apikey

        base_url = normalize_base_url(base_url)
        self.data_policy_api = DataPolicyApi(base_url, self.apikey, client=self.client)
