import uuid
from typing import List

from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import User, UserList, UserRequest, Search, Change


class UserApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v1/users")
    def list_users(self, limit: Query('limit') = 1000,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[User]:
        """
        This method retrieves a list of users with an optional limit on the number of results.

        Parameters:
            limit (Query): The maximum number of users to return. Defaults to 1000.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            List[User]: A list of user objects, where each User includes:
                - field_links (Links, optional): Hypermedia links associated with the user.
                - cid (str, optional): The unique identifier for the user within the CID context.
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tags (List[str], optional): Tags associated with the user.
                - tokens (List[TokenV2], optional): Tokens associated with the user.
                - type (str, optional): The type of the user.
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/users")
    def create_user(self, payload: Body(type=UserRequest),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> User:
        """
        This method creates a new user.

        Parameters:
            payload (Body): The request body containing the details of the user to be created.
                The UserRequest object includes:
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tokens (Dict[str, str], optional): A dictionary of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
                - user_id (str, optional): The unique user identifier.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            User: The created user object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the user.
                - cid (str, optional): The unique identifier for the user in the CID context.
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tags (List[str], optional): A list of tags associated with the user.
                - tokens (List[TokenV2], optional): A list of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/users/user-filters")
    def list_filtered_users(self, payload: Body(type=Search),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[User]:
        """
        This method retrieves users filtered by specific criteria.

        Parameters:
            payload (Body): The request body containing the filter criteria.
                The Search object includes:
                - cid (str, optional): The CID to filter by.
                - id (str, optional): The user ID to filter by.
                - tag (str, optional): A tag to filter users by.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            List[User]: A list of user objects, where each User includes:
                - field_links (Links, optional): Hypermedia links associated with the user.
                - cid (str, optional): The unique identifier for the user in the CID context.
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tags (List[str], optional): A list of tags associated with the user.
                - tokens (List[TokenV2], optional): A list of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/users/{user_id}")
    def get_user(self, user_id: str,
                 correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> User:
        """
        This method retrieves the details of a specific user by their ID.

        Parameters:
            user_id (str): The unique identifier of the user to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            User: The user object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the user.
                - cid (str, optional): The unique identifier for the user in the CID context.
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tags (List[str], optional): A list of tags associated with the user.
                - tokens (List[TokenV2], optional): A list of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @headers({"Content-Type": "application/json"})
    @put("api/v1/users/{user_id}")
    def update_user(self, user_id: str, payload: Body(type=UserRequest),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> User:
        """
        This method updates the details of an existing user.

        Parameters:
            user_id (str): The unique identifier of the user to update.
            payload (Body): The request body containing the updated user details.
                The UserRequest object includes:
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tokens (Dict[str, str], optional): A dictionary of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
                - user_id (str, optional): The unique identifier of the user.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            User: The updated user object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the user.
                - cid (str, optional): The unique identifier for the user in the CID context.
                - email (str, optional): The email address of the user.
                - federated_connector_id (str, optional): The federated connector ID associated with the user.
                - federated_user_id (str, optional): The federated user ID.
                - id (str, optional): The unique identifier of the user.
                - name (str, optional): The full name of the user.
                - properties (List[KeyValue], optional): A list of key-value properties associated with the user.
                - tags (List[str], optional): A list of tags associated with the user.
                - tokens (List[TokenV2], optional): A list of tokens associated with the user.
                - type (str, optional): The type of the user (e.g., "standard", "federated").
        """
        pass


    @raise_for_status_code
    @delete("api/v1/users/{user_id}")
    def delete_user(self, user_id: str,
                 correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4()))-> None:
        """
        This method deletes a user by their unique identifier.

        Parameters:
            user_id (str): The unique identifier of the user to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/users/{user_id}/changes")
    def list_user_changes(self, user_id: str,
                correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Change]:
        """
        This method retrieves a list of changes associated with a specific user.

        Parameters:
            user_id (str): The unique identifier of the user to get changes for.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Change]: A list of changes associated with the user, where each Change includes:
                - id (str, optional): The unique identifier of the change.
                - object_id (str, optional): The ID of the object associated with the change.
                - object_type (str, optional): The type of the object associated with the change.
                - subject_id (str, optional): The ID of the subject associated with the change.
                - details (str, optional): Additional details about the change.
                - what (str, optional): A description of what changed.
                - created_at (str, optional): The timestamp when the change was made.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/users")
    def list_users_v2(self,
                correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> UserList:
        """
        This method retrieves a paginated list of users.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID generated using the uuid.uuid4() method.

        Returns:
            UserList: A paginated list of users, where the UserList object includes:
                - page (int, optional): The current page number.
                - size (int, optional): The number of users per page.
                - total_pages (int, optional): The total number of pages.
                - total_records (int, optional): The total number of user records.
                - users (List[UserThinResponse], optional): A list of thin user response objects, where each UserThinResponse includes:
                    - email (str, optional): The email address of the user.
                    - id (str, optional): The unique identifier of the user.
                    - name (str, optional): The full name of the user.
                    - type (str, optional): The type of the user (e.g., "standard", "federated").
        """
        pass
