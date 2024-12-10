import uuid

from uplink import *
from typing import List
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import ThinSecret, Secret


class SecretApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/secrets")
    def list_secrets(self, entity: Query('entity') =  None, secret: Query('secret') =  None,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[ThinSecret]:
        """
        This method retrieves a list of all secrets with optional query filters.

        Parameters:
            entity (str, optional): A query parameter to filter secrets by the associated entity.
            secret (str, optional): A query parameter to filter secrets by a specific secret name.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[ThinSecret]: A list of thin secret objects, where each object includes:
                - id (str, optional): The unique identifier of the secret.
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/secrets")
    def create_secret(self, payload: Body(type=Secret),
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Secret:
        """
        This method creates a new secret.

        Parameters:
            payload (Body): The request body containing the details of the secret to be created.
                The Secret object includes:
                - field_links (Links, optional): Hypermedia links associated with the secret.
                - data (List[SecretEntry], optional): A list of secret entries, where each entry includes:
                    - key (str, optional): The key of the secret entry.
                    - base64Value (str, optional): The value of the secret entry in Base64-encoded format.
                - id (str, optional): The unique identifier of the secret.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Secret: The created secret object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the secret.
                - data (List[SecretEntry], optional): A list of secret entries, where each entry includes:
                    - key (str, optional): The key of the secret entry.
                    - base64Value (str, optional): The value of the secret entry in Base64-encoded format.
                - id (str, optional): The unique identifier of the secret.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/secrets/{id}")
    def get_secret(self, id: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Secret:
        """
        This method retrieves the details of a specific secret by its ID.

        Parameters:
            id (str): The unique identifier of the secret to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Secret: The details of the specified secret, which includes:
                - field_links (Links, optional): Hypermedia links associated with the secret.
                - data (List[SecretEntry], optional): A list of secret entries, where each entry includes:
                    - key (str, optional): The key of the secret entry.
                    - base64Value (str, optional): The value of the secret entry in Base64-encoded format.
                - id (str, optional): The unique identifier of the secret.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/secrets/{id}")
    def delete_secret(self, id: str,
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific secret by its ID.

        Parameters:
            id (str): The unique identifier of the secret to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass