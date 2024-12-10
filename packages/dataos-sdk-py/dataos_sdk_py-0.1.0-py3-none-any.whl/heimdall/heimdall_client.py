from commons.http.client.base_client import BaseHTTPClientBuilder
from commons.utils.helper import normalize_base_url
from heimdall.apis.authorize_api import AuthorizeApi
from heimdall.apis.policy_api import PolicyApi
from heimdall.apis.policy_use_case_grants_api import PolicyUseCaseGrantsApi
from heimdall.apis.policy_use_case_grant_requests import PolicyUseCaseGrantRequestsApi
from heimdall.apis.policy_enforcement_provider_api import PolicyEnforcementProviderApi
from heimdall.apis.roles_api import RolesApi
from heimdall.apis.secret_api import SecretApi
from heimdall.apis.tags_api import TagsApi
from heimdall.apis.tokens_api import TokensApi
from heimdall.apis.user_api import UserApi
from heimdall.apis.data_policy_api import DataPolicyApi
from heimdall.apis.collections_api import CollectionApi

class HeimdallClientBuilder(BaseHTTPClientBuilder):
    def get_default_user_agent_suffix(self):
        return "HeimdallClient"

    def build(self):
        """
        Build the HeimdallClient instance.

        Returns:
            HeimdallClient: An instance of HeimdallClient with the configured settings.
        """
        return HeimdallClient(self.base_url, self.apikey, self.get_http_client())


class HeimdallClient:
    def __init__(self, base_url, apikey, client=None):
        self.client = client
        self.base_url = base_url
        self.apikey = apikey
        """
        Initialize the HeimdallClient.

        This class provides a client to interact with various API endpoints related to Heimdall.

        Parameters:
            base_url (str): The base URL of the Heimdall API.
            apikey (str): The API key for authentication with the Heimdall API.
            client (object, optional): An instance of the HTTP client to use for making API requests (default is None).

        Attributes:
            secret_api (SecretApi): An instance of SecretApi for interacting with the Secret API endpoints.
            user_api (UserApi): An instance of UserApi for interacting with the User API endpoints.
            policy_api (PolicyApi): An instance of PolicyApi for interacting with the Policy API endpoints.
            authorize_api (AuthorizeApi): An instance of AuthorizeApi for interacting with the Authorize API endpoints.
            tags_api (TagsApi): An instance of TagsApi for interacting with the Tag API endpoints.
            tokens_api (TokensApi): An instance of TokensApi for interacting with the Token API endpoints.
            policy_use_case_grants_api (PolicyUseCaseGrantsApi): An instance of PolicyUseCaseGrantsApi for interacting 
                with the Policy Use Case Grant API endpoints.
            policy_use_case_grant_requests_api (PolicyUseCaseGrantRequestsApi): An instance of 
                PolicyUseCaseGrantRequestsApi for interacting with the Policy Use Case Grant Request API endpoints.
            roles_api (RolesApi): An instance of RolesApi for interacting with the Role API endpoints.
            policy_enforcement_provider_api (PolicyEnforcementProviderApi): An instance of PolicyEnforcementProviderApi 
                for interacting with the Policy Enforcement Provider API endpoints.
            data_policy_api (DataPolicyApi): An instance of DataPolicyApi for interacting with the Data Policy API endpoints.
            collection_api (CollectionApi): An instance of CollectionApi for interacting with the Collection API endpoints.
        """
        base_url = normalize_base_url(base_url)
        self.secret_api = SecretApi(base_url, self.apikey, client=self.client)
        self.user_api = UserApi(base_url, self.apikey, client=self.client)
        self.policy_api = PolicyApi(base_url, self.apikey, client=self.client)
        self.authorize_api = AuthorizeApi(base_url, self.apikey, client=self.client)
        self.tags_api = TagsApi(base_url, self.apikey, client=self.client)
        self.tokens_api = TokensApi(base_url, self.apikey, client=self.client)
        self.policy_use_case_grants_api = PolicyUseCaseGrantsApi(base_url, self.apikey, client=self.client)
        self.policy_use_case_grant_requests_api = PolicyUseCaseGrantRequestsApi(base_url, self.apikey, client=self.client)
        self.roles_api = RolesApi(base_url, self.apikey, client=self.client)
        self.policy_enforcement_provider_api = PolicyEnforcementProviderApi(base_url, self.apikey, client=self.client)
        self.data_policy_api = DataPolicyApi(base_url, self.apikey, client=self.client)
        self.collection_api = CollectionApi(base_url, self.apikey, client=self.client)