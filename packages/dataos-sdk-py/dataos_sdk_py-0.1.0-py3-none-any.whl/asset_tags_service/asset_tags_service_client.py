from asset_tags_service.apis.asset_tags_api import AssetTagsApi
from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url


class AssetTagsServiceClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "AssetTagsServiceClient"

    def build(self):
        """
        Build the AssetTagsServiceClient instance.

        Returns:
            AssetTagsServiceClient: An instance of AssetTagsServiceClient with the configured settings.
        """
        return AssetTagsServiceClient(self.base_url, self.apikey, self.get_http_client())


class AssetTagsServiceClient:
    def __init__(self, base_url, apikey, client=None):
        self.client = client
        self.base_url = base_url
        self.apikey = apikey
        """
        Initialize the AssetTagsServiceClient.

        This class provides a client to interact with the Asset Tags Service API for managing asset tags.

        Parameters:
            base_url (str): The base URL of the Asset Tags Service API.
            apikey (str): The API key for authentication with the Asset Tags Service API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            asset_tags_api (AssetTagsApi): An instance of AssetTagsApi for interacting with the Asset Tags API endpoints.
        """
        base_url = normalize_base_url(base_url)
        self.asset_tags_api = AssetTagsApi(base_url, self.apikey, client=self.client)
