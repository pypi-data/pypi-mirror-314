import uuid

from typing import List

from uplink import Header, get, returns, post, delete, Body, headers

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import Role, Change


class RolesApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/roles")
    def list_roles(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Role]:
        """
        This method retrieves a list of all roles.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Role]: A list of role objects, where each role includes:
                - id (str, optional): The unique identifier of the role.
                - name (str, optional): The name of the role.
                - description (str, optional): A human-readable description of the role.
                - tag (str, optional): A tag associated with the role.
        """
        pass

    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/roles")
    def create_role(self, payload: Body(type=Role),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Role:
        """
        This method creates a new role.

        Parameters:
            payload (Body): The request body containing the details of the role to be created.
                The Role object includes:
                - name (str, required): The name of the role.
                - description (str, optional): A human-readable description of the role.
                - tag (str, optional): A tag associated with the role.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Role: The created role object, which includes:
                - id (str, optional): The unique identifier of the role.
                - name (str, optional): The name of the role.
                - description (str, optional): A human-readable description of the role.
                - tag (str, optional): A tag associated with the role.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/roles/{id}")
    def get_role_by_id(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Role:
        """
        This method retrieves the details of a specific role by its ID.

        Parameters:
            id (str): The unique identifier of the role to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Role: The details of the specified role, which includes:
                - id (str, optional): The unique identifier of the role.
                - name (str, optional): The name of the role.
                - description (str, optional): A human-readable description of the role.
                - tag (str, optional): A tag associated with the role.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/roles/{id}")
    def delete_role(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific role by its ID.

        Parameters:
            id (str): The unique identifier of the role to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/roles/{id}/changes")
    def get_role_changes(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Change]:
        """
        This method retrieves a list of changes associated with a specific role by its ID.

        Parameters:
            id (str): The unique identifier of the role to retrieve changes for.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Change]: A list of changes associated with the role, where each change includes:
                - id (str, optional): The unique identifier of the change.
                - object_id (str, optional): The ID of the object associated with the change.
                - object_type (str, optional): The type of the object associated with the change.
                - subject_id (str, optional): The ID of the subject associated with the change.
                - details (str, optional): Additional details about the change.
                - what (str, optional): A description of what changed.
                - created_at (str, optional): The timestamp when the change was made.
        """
        pass