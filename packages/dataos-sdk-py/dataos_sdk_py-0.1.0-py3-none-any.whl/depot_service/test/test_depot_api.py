import unittest
from depot_service.depot_service_client import DepotServiceClientBuilder
from commons.utils.env_helper import get_env_or_throw


class TestDepotApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        # Create an instance of ResolveApi with a mock DepotServiceClient
        base_url = f"https://{get_env_or_throw('DATAOS_FQDN')}/ds"
        api_key = get_env_or_throw("DATAOS_RUN_AS_APIKEY")
        self.tenant = get_env_or_throw("DATAOS_TENANT_ID")
        self.ds_client = (DepotServiceClientBuilder().
                          set_base_url(base_url).
                          set_apikey(api_key).build())
        self.mock_request = {
            "type": "postgresql",
            "external": False,
            "description": "Test description",
            "owners": ["owner1", "owner2"],
            "meta": {"key": {"info": "meta data"}},
            "source": "source_name",
            "isArchived": False,
            "postgresql": {
                "subprotocol": "jdbc",
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "params": {
                    "ssl": {"enabled": True},
                    "retries": {"max": 3}
                }
            }
        }
        self.mock_response = {
            "name": "testdepot",
            "type": "postgresql",
            "external": False,
            "description": "Test description",
            "owners": ["owner1", "owner2"],
            "meta": {"key": {"info": "meta data"}},
            "source": "source_name",
            "isArchived": False,
            "postgresql": {
                "subprotocol": "jdbc",
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "params": {
                    "ssl": {"enabled": True},
                    "retries": {"max": 3}
                }
            }
        }

    def test_create_or_update_depot(self, ):
        # Call the method
        result = self.ds_client.depot_api.create_or_update(tenant=self.tenant, depot='testdepot', payload=self.mock_request)

        # Assertions
        self.assertEqual(result.name, "testdepot")
        self.assertEqual(result.type, "postgresql")
        self.assertFalse(result.external)
        self.assertEqual(result.owners, ["owner1", "owner2"])
        self.assertEqual(result.meta["key"]["info"], "meta data")
        self.assertFalse(result.isArchived)

    def test_get_depot(self):
        # Call the method
        result = self.ds_client.depot_api.get_depot(tenant='engineering', depot='devslakehouse')
        # Assertions
        self.assertEqual(result['name'], "testdepot")
        self.assertEqual(result['type'], "postgresql")
        self.assertFalse(result['external'])
        self.assertEqual(result['owners'], ["owner1", "owner2"])
        self.assertEqual(result['meta']["key"]["info"], "meta data")
        self.assertFalse(result['isArchived'])
        self.assertEqual(result['postgresql']["host"], "localhost")
        self.assertEqual(result['postgresql']["port"], 5432)
        self.assertEqual(result['postgresql']["database"], "test_db")
        self.assertTrue(result['postgresql']["params"]["ssl"]["enabled"])
        self.assertEqual(result['postgresql']["params"]["retries"]["max"], 3)

    def test_get_meta(self):
        # Call the method
        result = self.ds_client.depot_api.get_meta(tenant=self.tenant, depot='testdepot')

        # Assertions
        self.assertEqual(result['key']['info'], "meta data")

    def test_add_update_meta(self):
        # Create a payload for updating the meta
        payload = {"key": {"info": "updated meta data"}}

        # Call the add_update_meta method
        result = self.ds_client.depot_api.add_update_meta(tenant=self.tenant, depot='testdepot', payload=payload)

        print(result)
        # Assertions
        assert result['key']['info'] == "updated meta data"

if __name__ == "__main__":
    unittest.main()
