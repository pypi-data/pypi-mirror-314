import unittest
from depot_service.depot_service_client import DepotServiceClientBuilder
from commons.utils.env_helper import get_env_or_throw


class TestSecretApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        # Create an instance of ResolveApi with a mock DepotServiceClient
        base_url = f"https://{get_env_or_throw('DATAOS_FQDN')}/ds"
        api_key = get_env_or_throw("DATAOS_RUN_AS_APIKEY")
        self.ds_client = (DepotServiceClientBuilder().
                          set_base_url(base_url).
                          set_apikey(api_key).build())

    def test_secret_with_depot_service_client(self):
        secret_id = 'icebase_rw_rw'
        result = self.ds_client.secret_api.get_secrets(secret=secret_id)

        assert 'id' in result.model_dump()
        assert 'data' in result.model_dump()


if __name__ == "__main__":
    unittest.main()
