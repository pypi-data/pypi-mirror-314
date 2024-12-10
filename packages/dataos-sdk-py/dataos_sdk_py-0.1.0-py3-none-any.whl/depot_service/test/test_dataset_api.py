import unittest
from depot_service.depot_service_client import DepotServiceClientBuilder
from commons.utils.env_helper import get_env_or_throw


class TestDepotApiWithDepotServiceClient(unittest.TestCase):

    def setUp(self):
        # Create an instance of ResolveApi with a mock DepotServiceClient
        base_url = f"https://{get_env_or_throw('DATAOS_FQDN')}/ds"
        api_key = get_env_or_throw("DATAOS_RUN_AS_APIKEY")
        self.ds_client = (DepotServiceClientBuilder().
                          set_base_url(base_url).
                          set_apikey(api_key).build())
        self.tenant = get_env_or_throw("DATAOS_TENANT_ID")

    def test_all_or_update_depot(self):
        depot = "icebase"
        collection = "retail"
        dataset = "city"
        branch = "main"
        new_branch = "new_branch"
        snapshotId = "4083978310859215289"

        # # List branches
        # result: str = self.ds_client.dataset_api.list_branches(depot=depot, collection=collection, dataset=dataset)
        # print(result)
        #
        # # List branch snapshots
        # result = self.ds_client.dataset_api.list_branch_snapshots(depot=depot, collection=collection, dataset=dataset,
        #                                                           branch="main")
        # print(result)
        #
        # result = self.ds_client.dataset_api.list_snapshots(depot=depot, collection=collection, dataset=dataset)
        # print(result)
        #
        # # result = self.ds_client.dataset_api.create_branch(depot=depot, collection=collection, dataset=dataset,
        # #                                                   branch=new_branch,
        # #                                                   payload={"snapshotId": snapshotId})
        # # print(result)
        #
        # result: str = self.ds_client.dataset_api.list_branches(depot=depot, collection=collection, dataset=dataset)
        # print(result)
        #
        # # result = self.ds_client.dataset_api.rename_branch(depot=depot, collection=collection, dataset=dataset,
        # #                                                   branch='testing2',
        # #                                                   payload={'name': 'testing3'})
        # # print(result)
        #
        # result = self.ds_client.dataset_api.list_branches(depot=depot, collection=collection, dataset=dataset)
        # print(result)
        #
        # result = self.ds_client.dataset_api.replace_branch(depot=depot, collection=collection, dataset=dataset,
        #                                                    branch='testing3',
        #                                                    payload={'sourceBranch': 'main',
        #                                                             'snapshotId': '508082190766355723'})
        # print(result)
        #
        # result = self.ds_client.dataset_api.list_branches(depot=depot, collection=collection, dataset=dataset)
        # print(result)
        #
        # result = self.ds_client.dataset_api.show_schema_update(depot=depot, collection=collection, dataset=dataset, branch="main")
        # print(result)

        result = self.ds_client.dataset_api.show_branch_stats(tenant=self.tenant, depot=depot, collection=collection, dataset=dataset,
                                                              branch="main")
        print(result)


if __name__ == "__main__":
    unittest.main()
