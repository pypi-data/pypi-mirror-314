import unittest

from commons.utils.env_helper import get_env_or_throw
from depot_service.depot_service_client import DepotServiceClientBuilder


class TestResolveApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        base_url = f"https://{get_env_or_throw('DATAOS_FQDN')}/ds"
        api_key = get_env_or_throw("DATAOS_RUN_AS_APIKEY")
        self.ds_client = (DepotServiceClientBuilder().
                          set_base_url(base_url).
                          set_apikey(api_key).build())
        self.tenant = get_env_or_throw("DATAOS_TENANT_ID")

    def test_resolve_v2_address_with_depot_service_client(self):
        # Mock the response data from the DepotServiceClient
        response_data = {'depot': 'icebase', 'type': 'abfss', 'collection': 'retail', 'dataset': 'city',
                         'format': 'iceberg', 'external': False, 'isArchived': False, 'source': 'icebase',
                         'connection': {}, 'secrets': []}

        address = "dataos://icebase:retail/city"
        resolved_address = self.ds_client.resolve_api.resolve(tenant=self.tenant, address=address)
        assert all(key in response_data for key in resolved_address.model_dump())

    def test_resolve_v3_address_with_depot_service_client(self):
        # Mock the response data from the DepotServiceClient
        response_data = {'depot': 'icebase', 'type': 'abfss', 'collection': 'retail', 'dataset': 'city',
                          'format': 'iceberg', 'external': False, 'isArchived': False, 'source': 'icebase',
                          'secrets': [], 'abfss': {}, 'bigquery': None, 'elasticsearch': None, 'eventhub': None,
                          'file': None, 'gcs': None, 'http': None, 'jdbc': None, 'kafka': None, 'mongodb': None,
                          'mysql': None, 'opensearch': None, 'oracle': None, 'postgresql': None, 'presto': None,
                          'pulsar': None, 'redis': None, 'redshift': None, 's3': None, 'snowflake': None, 'wasbs': None,
                          'resolution': {}}

        address = "dataos://icebase:retail/city"
        resolved_address = self.ds_client.resolve_api.resolve_v3(tenant=self.tenant, address=address)
        assert all(key in response_data for key in resolved_address.model_dump())


if __name__ == "__main__":
    unittest.main()
