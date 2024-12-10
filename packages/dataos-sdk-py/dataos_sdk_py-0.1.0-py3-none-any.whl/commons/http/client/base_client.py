import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from commons.utils.helper import normalize_base_url


class BaseHTTPClientBuilder:
    def __init__(self):
        """
        Base HTTP Client Builder.

        This class provides a blueprint for building configurations for an HTTP client.

        Configurable Properties:
            base_url (str): The base URL of the API.
            apikey (str): The API key for authentication with the API.
            enable_ssl (bool): Whether to enable SSL for API requests (default is False).
            client (object): An instance of the HTTP client to use for making API requests.
            ssl_verify_hostname (bool): Whether to verify SSL hostname for API requests (default is True).
            keystore_path (str): The path to the keystore file for SSL (default is None).
            keystore_pass (str): The password for the keystore file (default is None).
            truststore_path (str): The path to the truststore file for SSL (default is None).
            truststore_pass (str): The password for the truststore file (default is None).
            connect_timeout (int): The connection timeout in milliseconds for API requests (default is 10000 ms).
            read_timeout (int): The read timeout in milliseconds for API requests (default is 10000 ms).
            user_agent (str): The user agent string to use for API requests.
            max_retries (int): The maximum number of times to retry API requests on failure (default is 3).
            backoff_factor (float): The backoff factor for retrying API requests on failure (default is 0.3).
            headers (dict): Additional headers to include in API requests (default is None).
        """
        self.base_url = None
        self.apikey = None
        self.enable_ssl = True
        self.client = None
        self.ssl_verify_hostname = True
        self.keystore_path = None
        self.keystore_pass = None
        self.truststore_path = None
        self.truststore_pass = None
        self.connect_timeout = 10000
        self.read_timeout = 10000
        self.user_agent = None
        self.max_retries = 3
        self.backoff_factor = 0.3
        self.headers = None

    def get_http_client(self):
        return self.client or self.build_http_client()

    def get_user_agent(self):
        return self.user_agent or f"dataos-sdk-py/{self.get_default_user_agent_suffix()}"

    def get_default_user_agent_suffix(self):
        raise NotImplementedError("Subclasses must implement this method to provide the default user agent suffix.")

    def set_base_url(self, base_url):
        self.base_url = normalize_base_url(base_url)
        return self

    def set_user_agent(self, user_agent):
        self.user_agent = user_agent
        return self

    def set_apikey(self, apikey):
        self.apikey = apikey
        return self

    def set_enable_ssl(self, enable_ssl):
        self.enable_ssl = enable_ssl
        return self

    def set_ssl_verify_hostname(self, verify_hostname):
        self.ssl_verify_hostname = verify_hostname
        return self

    def set_keystore_path(self, keystore_path):
        self.keystore_path = keystore_path
        return self

    def set_keystore_pass(self, keystore_pass):
        self.keystore_pass = keystore_pass
        return self

    def set_truststore_path(self, truststore_path):
        self.truststore_path = truststore_path
        return self

    def set_truststore_pass(self, truststore_pass):
        self.truststore_pass = truststore_pass
        return self

    def set_connect_timeout(self, timeout):
        self.connect_timeout = timeout
        return self

    def set_read_timeout(self, timeout):
        self.read_timeout = timeout
        return self

    def set_max_retries(self, max_retries):
        self.max_retries = max_retries
        return self

    def set_backoff_factor(self, backoff_factor):
        self.backoff_factor = backoff_factor
        return self

    def build_headers(self, headers):
        headers_ = {"User-Agent": self.get_user_agent()}
        if self.apikey:
            headers_["apikey"] = self.apikey
        if headers:
            headers_.update(headers)
        return headers_

    def build_http_client(self):
        """
        Build and configure an HTTP client.

        Returns:
            requests.Session: An instance of the configured HTTP client.
        """
        session = requests.Session()
        if self.enable_ssl and self.ssl_verify_hostname:
            session.verify = True
            if self.keystore_path or \
                    self.keystore_pass or \
                    self.truststore_path or \
                    self.keystore_pass:
                # SSL with custom keystore and truststore
                session.cert = (self.keystore_path, self.keystore_pass)
                session.verify = self.truststore_path
        else:
            session.verify = False

        if self.max_retries > 0:
            retry_strategy = Retry(
                total=self.max_retries,
                backoff_factor=self.backoff_factor,
                status_forcelist=[500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

        self.client = session
        self.client.headers.update(self.build_headers(self.headers))
        return self.client
