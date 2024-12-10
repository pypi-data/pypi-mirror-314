from __future__ import absolute_import

import uuid
from typing import Dict, List

from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from depot_service.models.ds_models import FieldRequest, DatasetRequest, DatasetResponse, IcebergPartitionSpecRequest, \
    IcebergStats, MetadataVersionResponse, SnapshotResponse, FieldRenameRequest, FieldUpdateRequest, \
    BranchCreateRequest, FastForwardRequest, RenameBranchRequest, ReplaceBranchRequest


class DatasetApi(DataOSBaseConsumer):
    @json
    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/fields")
    def add_field(self, tenant: str, depot: str, collection: str, dataset: str, payload: Body(type=FieldRequest),
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Adds a new field to a dataset within the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            payload (Body): The field request data, as a FieldRequest object.
                - **Attributes**:
                    - `name` (str): The name of the new field (required).
                    - `type` (str): The data type of the new field (e.g., string, integer).
                    - `precision` (Optional[int]): Total number of significant digits for numeric fields.
                    - `scale` (Optional[int]): Number of digits to the right of the decimal for numeric fields.
                    - `keyType` (Optional[str]): Type of key (e.g., primary key, foreign key).
                    - `valueType` (Optional[str]): Specifies the type of values the field will hold (e.g., text, number).

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @delete("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}")
    def drop_field(self, tenant: str, depot: str, collection: str, dataset: str, field: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Drops a field from a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            field (str): The name of the field to be dropped.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def fetch_dataset(self, tenant: str, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DatasetResponse:
        """
        Fetches a dataset from the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch.

        Returns:
            DatasetResponse: An instance of the DatasetResponse class representing the fetched dataset.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @json
    @post("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def create_dataset(self, tenant: str, depot: str, collection: str, dataset: str, payload: Body(type=DatasetRequest),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Creates a new dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the new dataset to be created.
            payload (Body): The dataset request data, as a DatasetRequest object.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @delete("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}")
    def drop_dataset(self, tenant: str, depot: str, collection: str, dataset: str, purge: Query('purge') = False,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Drops (deletes) a dataset from the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to drop.
            purge (Query): An optional query parameter to indicate whether to purge the dataset completely.
                - Default: False

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/partitions")
    def update_partition(self, tenant: str, depot: str, collection: str, dataset: str,
                         payload: Body(type=List[IcebergPartitionSpecRequest]),
                         correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Updates partitions for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to update partitions.
            payload (Body): The payload containing the partition specification request data.
                - type (List[IcebergPartitionSpecRequest]): A list of partition specification requests.
                    - **Attributes**:
                        - `index` (int): The index of the partition specification.
                        - `type` (str): The type of partitioning, e.g., "hash", "range", etc.
                        - `column` (str): The name of the column to use for partitioning.
                        - `name` (Optional[str]): The optional name of the partition.
                        - `num_buckets` (Optional[int]): The optional number of buckets for "hash" partitioning.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/schema")
    def fetch_schemas(self, tenant: str, depot: str, collection: str, dataset: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Fetches the schema of a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch the schema.

        Returns:
            str: A JSON string representing the schema of the dataset.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets")
    def list_dataset(self, tenant: str, depot: str, collection: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Method to list datasets in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.

        Returns:
            List[str]: A list of dataset names available in the specified collection.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/stats")
    def show_stats(self, tenant: str, depot: str, collection: str, dataset: str, groupBy: Query('groupBy') = None,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> IcebergStats:
        """
        Method to retrieve statistics for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to retrieve statistics.

        Returns:
            IcebergStats: An instance of the IcebergStats data model representing the dataset statistics.
                Attributes:
                    stats (Dict[str, str]): A dictionary containing general statistics for the dataset.
                    timeline (Dict[str, Dict[str, str]]): A dictionary representing the timeline of statistics.
                    properties (Dict[str, str]): A dictionary containing additional properties related to statistics.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def list_properties(self, tenant: str, depot: str, collection: str, dataset: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Dict[str, str]:
        """
        Method to list properties of a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list properties.

        Returns:
            Dict[str, str]: A dictionary representing the properties of the dataset.
        """
        pass

    @raise_for_status_code
    @json
    @delete("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def remove_properties(self, tenant: str, depot: str, collection: str, dataset: str, payload: Body(List[str]),
                          correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to remove properties from a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset from which properties should be removed.
            payload (Body): The payload containing a list of property names to be removed.
                - type (List[str]): The list of property names to remove.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/properties")
    def add_properties(self, tenant: str, depot: str, collection: str, dataset: str, payload: Body(Dict[str, str]),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to add properties to a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to which properties should be added.
            payload (Body): The payload containing a dictionary of property names and values to add.
                - type (Dict[str, str]): A dictionary of property names and their corresponding values.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/metadata")
    def list_metadata(self, tenant: str, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[
        MetadataVersionResponse]:
        """
        Method to list metadata versions for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list metadata versions.

        Returns:
            List[MetadataVersionResponse]: A list of MetadataVersionResponse objects representing metadata versions.
                Attributes:
                version (str): The version string representing the metadata version.
                timestamp (int): The timestamp associated with the metadata version.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/metadata/{version}")
    def set_metadata(self, tenant: str, depot: str, collection: str, dataset: str, version: str,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to set metadata for a specific version of a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset for which metadata should be set.
            version (str): The version of the metadata file to be set.
                Valid options: "latest" for the latest version,
                               "v2.metadata.json" for a specific version,
                               "v2.gz.metadata.json" for a specific version (compressed).

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/nullable/{nullable}")
    def update_nullability(self, tenant: str, depot: str, collection: str, dataset: str, field: str, nullable: bool,
                           correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to update the nullability of a field in the specified dataset of a collection within a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field.
            field (str): The name of the field for which the nullability should be updated.
            nullable (bool): The new nullability status of the field. Set to True to make the field nullable,
                             or False to make it non-nullable.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/snapshots")
    def list_snapshots(self, tenant: str, depot: str, collection: str, dataset: str,
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[SnapshotResponse]:
        """
        Method to list snapshots for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to list snapshots.

        Returns:
            List[SnapshotResponse]: A list of SnapshotResponse objects representing the snapshots.
        """
        pass

    @raise_for_status_code
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/snapshots/{id}")
    def set_snapshot(self, tenant: str, depot: str, collection: str, dataset: str, id: int,
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to set a specific snapshot for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset for which the snapshot should be set.
            id (int): The ID of the snapshot to be set.
                eg: 566136990417338097

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/rename")
    def rename_field(self, tenant: str, depot: str, collection: str, dataset: str, field: str,
                     payload: Body(type=FieldRenameRequest),
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to rename a field in the specified dataset of a collection within a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field to be renamed.
            field (str): The name of the field to be renamed.
            payload (Body): The payload containing the new name of the field.
                - type (FieldRenameRequest): The request body with the new field name.
                  It should have the following attribute:
                  - new_name (str): The new name for the field.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/fields/{field}/update")
    def update_field(self, tenant: str, depot: str, collection: str, dataset: str, field: str,
                     payload: Body(type=FieldUpdateRequest),
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to update properties of a field in the specified dataset of a collection within a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset containing the field to be updated.
            field (str): The name of the field to be updated.
            payload (Body): The payload containing the updated properties of the field.
                - type (FieldUpdateRequest): The request body with the updated properties of the field.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @post("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}")
    def create_namespace(self, tenant: str, depot: str, collection: str,
                         correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to create a new namespace (collection) within a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the new collection (namespace) to create.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/schemas")
    def fetch_schemas(self, tenant: str, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Method to fetch schemas for a dataset in the specified collection of a depot.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset to fetch schemas.

        Returns:
            str: The schemas for the specified dataset in JSON format.
        """
        pass

    @raise_for_status_code
    @returns.json
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/cherrypick/{snapshotId}")
    def cherry_pick_snapshot(self, tenant: str, depot: str, collection: str, dataset: str, snapshotId: str,
                             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Method to Cherry-picks a specific snapshot for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            snapshotId (str): The ID of the snapshot to be cherry-picked.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @post("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}")
    def create_branch(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                      payload: Body(type=BranchCreateRequest),
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Creates a new branch for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the new branch.
            payload (Body): The branch creation request data, as BranchCreateRequest object.
                - **Attributes**:
                    - `snapshotId` (int): The ID of the snapshot to base the branch on.

        Returns:
            None: This method does not return anything.
        """

        pass

    @raise_for_status_code
    @delete("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}")
    def delete_branch(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Deletes a branch for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the branch to be deleted.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}/fastforward")
    def fast_forward_branch(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                            payload: Body(type=FastForwardRequest),
                            correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Fast-forwards a branch to a specific state for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the branch to fast-forward.
            payload (Body): The fast-forward request data, as FastForwardRequest object.
                - **Attributes**:
                    - `name` (str): The target name or identifier for the fast-forward operation.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}/snapshots")
    def list_branch_snapshots(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                              correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Lists all snapshots for a given branch of an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the branch.

        Returns:
            List[str]: A list of snapshot IDs.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches")
    def list_branches(self, tenant: str, depot: str, collection: str, dataset: str,
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        Lists all branches for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.

        Returns:
            List[str]: A list of branch names.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}/rename")
    def rename_branch(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                      payload: Body(type=RenameBranchRequest),
                      correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Renames a branch for an iceberg dataset.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The current name of the branch.
            payload (Body): The branch renaming request data, as RenameBranchRequest object.
                - **Attributes**:
                    - `name` (str): The new name for the branch.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @headers({"Content-Type": "application/json"})
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/branches/{branch}/replace")
    def replace_branch(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                       payload: Body(type=ReplaceBranchRequest),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
         Replaces a branch for an iceberg dataset.

         Parameters:
             tenant (str): The name of the tenant.
             depot (str): The name of the depot.
             collection (str): The name of the collection within the depot.
             dataset (str): The name of the dataset within the collection.
             branch (str): The name of the branch to replace.
             payload (Body): The branch replacement request data, as ReplaceBranchRequest object.
                 - **Attributes**:
                     - `sourceBranch` (str): The source branch for replacement.
                     - `snapshotId` (str): The snapshot ID to replace the branch with.

         Returns:
             None: This method does not return anything.
         """
        pass

    @raise_for_status_code
    @json
    @patch("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/rollback/{id}")
    def rollback_snapshot(self, tenant: str, depot: str, collection: str, dataset: str, id: int,
                          correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Rolls back a dataset to a specific snapshot state.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            id (int): The snapshot ID to roll back to.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/stats/branches/{branch}/schemaUpdates")
    def show_schema_update(self, tenant: str, depot: str, collection: str, dataset: str, branch: str,
                           correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> str:
        """
        Retrieves schema updates statistics for a branch of an iceberg dataset in a timeline view.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the branch.

        Returns:
            str: The schema updates statistics in JSON format.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/depots/{depot}/collections/{collection}/datasets/{dataset}/stats/branches/{branch}")
    def show_branch_stats(self, tenant: str, depot: str, collection: str, dataset: str, branch: str, groupBy: Query('groupBy') = None,
                          correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> IcebergStats:
        """
        Retrieves statistics for a branch of an iceberg dataset in a timeline view.

        Parameters:
            tenant (str): The name of the tenant.
            depot (str): The name of the depot.
            collection (str): The name of the collection within the depot.
            dataset (str): The name of the dataset within the collection.
            branch (str): The name of the branch.
            groupBy (Optional[str]): An optional parameter to group the statistics by a specific attribute.

        Returns:
            IcebergStats: An instance of the IcebergStats data model representing the dataset statistics.
                Attributes:
                    stats (Dict[str, str]): A dictionary containing general statistics for the dataset.
                    timeline (Dict[str, Dict[str, str]]): A dictionary representing the timeline of statistics.
                    properties (Dict[str, str]): A dictionary containing additional properties related to statistics.
        """
        pass
