import uuid

from typing import List
from uplink import Header, get, returns, post, put, delete, Body, headers

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.data_policy_models import DataPolicy
from heimdall.models.datapolicy import Table

class DataPolicyApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("dp/api/v1/policies")
    def list_data_policies(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[DataPolicy]:
        """
        This method retrieves a list of data policies.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[DataPolicy]: A list of data policy objects, where each DataPolicy includes:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("dp/api/v1/policies")
    def create_data_policy(self, payload: Body(type=DataPolicy),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
        """
        This method creates a new data policy.

        Parameters:
            payload (DataPolicy): The data policy object to be created, containing the following fields:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            DataPolicy: The newly created data policy object, containing the following fields:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
        """

        pass


    @raise_for_status_code
    @returns.json
    @get("dp/api/v1/policies/dataset/{dataset_id}")
    def list_dataset_policies(self, dataset_id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[DataPolicy]:
        """
        Retrieves a list of data policies associated with a specific dataset using the Data Policy Service API.

        Parameters:
            dataset_id (str): The unique identifier for the dataset whose data policies are to be retrieved.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[DataPolicy]: A list of data policy objects, where each DataPolicy includes:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("dp/api/v1/policies/{id}")
    def get_data_policy(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
        """
        This method retrieves a specific data policy by its unique ID.

        Parameters:
            id (str): The unique identifier of the data policy to be retrieved.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            DataPolicy: The data policy object, containing the following fields:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @put("dp/api/v1/policies/{id}")
    def update_data_policy(self, id: str, payload: Body(type=DataPolicy),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
        """
        This method updates an existing data policy identified by its unique ID.

        Parameters:
            id (str): The unique identifier of the data policy to be updated.
            payload (DataPolicy): The updated data policy object, containing the following fields:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            DataPolicy: The updated data policy object, containing the following fields:
                - collection (str, optional): The collection to which the data policy applies.
                - dataset_id (str, optional): The identifier for the dataset associated with the policy.
                - description (str, optional): A description of the data policy.
                - filters (List[Filter], optional): A list of filters associated with the policy.
                - mask (masks.Mask, optional): The masking rules associated with the policy.
                - name (str, optional): The name of the data policy.
                - owner (str, optional): The owner of the data policy.
                - priority (int, optional): The priority of the data policy.
                - selector (Selector, optional): The selector specifying criteria for the policy.
                - type (str, optional): The type of the data policy.
        """
        pass


    @raise_for_status_code
    @delete("dp/api/v1/policies/{id}")
    def delete_data_policy(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes an existing data policy identified by its unique ID.

        Parameters:
            id (str): The unique identifier of the data policy to be deleted.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None: This method does not return any value upon successful deletion.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("dp/api/v1/policies/decisionExternalTruth")
    def make_data_policy_decision(self, payload: Body(type=Table),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Table:
        """
        This method makes a data policy decision for a given dataset.

        Parameters:
            payload (Table): The context for the data policy decision, containing the following fields:
                - columns (List[Column], optional): A list of columns in the dataset, where each Column includes:
                    - data_type (str, optional): The data type of the column.
                    - name (str, optional): The name of the column.
                    - tags (List[str], optional): Tags associated with the column.
                - id (str, optional): The unique identifier for the dataset.
                - tags (List[str], optional): Tags associated with the dataset.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Table: The resulting table after applying the data policy decision, containing the following fields:
                - columns (List[Column], optional): A list of columns in the dataset, where each Column includes:
                    - data_type (str, optional): The data type of the column.
                    - name (str, optional): The name of the column.
                    - tags (List[str], optional): Tags associated with the column.
                - id (str, optional): The unique identifier for the dataset.
                - tags (List[str], optional): Tags associated with the dataset.
        """
        pass