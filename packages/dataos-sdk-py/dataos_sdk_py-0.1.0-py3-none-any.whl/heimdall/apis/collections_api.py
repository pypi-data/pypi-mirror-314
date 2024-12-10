import uuid

from typing import List
from uplink import Header, get, returns, post, delete, Body, headers

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import Collection


class CollectionApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v2/collections")
    def list_collections(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Collection]:
        """
        This method retrieves a list of all collections.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Collection]: A list of collection objects, which include:
                - name (str, optional): The name of the collection.
                - description (str, optional): A human-readable description of the collection.
                - flavor (str, optional): The type or flavor of the collection.
                - access_policy_config (AccessPolicyConfig, optional): Configuration settings for the collection's access policy,
                  including default_allow (bool, optional) indicating the default access behavior.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v2/collections")
    def create_collection(self, payload: Body(type=Collection),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Collection:
        """
        This method creates a new collection.

        Parameters:
            payload (Body): The request body containing the details of the collection to be created.
                The Collection object includes:
                - name (str, optional): The name of the collection.
                - description (str, optional): A human-readable description of the collection.
                - flavor (str, optional): The type or flavor of the collection.
                - access_policy_config (AccessPolicyConfig, optional): Configuration settings for the collection's access policy,
                  including default_allow (bool, optional) indicating the default access behavior.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Collection: The created collection object, which includes:
                - name (str, optional): The name of the collection.
                - description (str, optional): A human-readable description of the collection.
                - flavor (str, optional): The type or flavor of the collection.
                - access_policy_config (AccessPolicyConfig, optional): Configuration settings for the collection's access policy,
                  including default_allow (bool, optional) indicating the default access behavior.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v2/collections/{name}")
    def get_collection(self, name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Collection:
        """
        This method retrieves the details of a specific collection by its name.

        Parameters:
            name (str): The name of the collection to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Collection: The details of the specified collection, which include:
                - name (str, optional): The name of the collection.
                - description (str, optional): A human-readable description of the collection.
                - flavor (str, optional): The type or flavor of the collection.
                - access_policy_config (AccessPolicyConfig, optional): Configuration settings for the collection's access policy,
                  including default_allow (bool, optional) indicating the default access behavior.
        """
        pass


    @raise_for_status_code
    @delete("api/v2/collections/{name}")
    def delete_collection(self, name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific collection by its name.

        Parameters:
            name (str): The name of the collection to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass
