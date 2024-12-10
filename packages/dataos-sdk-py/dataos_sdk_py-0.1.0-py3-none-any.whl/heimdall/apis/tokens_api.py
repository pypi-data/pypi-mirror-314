import uuid

from typing import List

from uplink import Header, get, returns, post, delete, Body, headers, json, Query

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import TokenV2, RotateTokenRequest, TokenRequest


class TokensApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/tokens")
    def retrieve_token_by_value(self, token: Query('token'),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TokenV2:
        """
        This method retrieves a token by its value.

        Parameters:
            token (str): The token value used to query the specific token details.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TokenV2: The retrieved token object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional data associated with the token as key-value pairs.
                - description (str, optional): A human-readable description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the user associated with the token.
        """
        pass


    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @json
    @post("api/v1/tokens")
    def rotate_token(self,  payload: Body(type=RotateTokenRequest),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TokenV2:
        """
        This method rotates an existing token to generate new one.

        Parameters:
            payload (Body): The request body containing the details of the token rotation.
                The RotateTokenRequest object includes:
                - duration (str, optional): The duration of the token in ISO 8601 format.
                - token (str, required): The value of the token to be rotated.
                - user_id (str, optional): The unique identifier of the user associated with the token.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TokenV2: The rotated token object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional data associated with the token as key-value pairs.
                - description (str, optional): A human-readable description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the user associated with the token.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/tokens/{token_name}")
    def retrieve_token_by_name(self, token_name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TokenV2:
        """
        This method retrieves the details of a token by its name.

        Parameters:
            token_name (str): The name of the token to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TokenV2: The retrieved token object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional data associated with the token as key-value pairs.
                - description (str, optional): A human-readable description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the user associated with the token.
        """
        pass


    @raise_for_status_code
    @delete("api/v1/tokens/{token_name}")
    def delete_token_by_name(self, token_name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a token by its name.

        Parameters:
            token_name (str): The name of the token to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/users/{user_id}/tokens")
    def list_user_tokens(self, user_id: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[TokenV2]:
        """
        This method retrieves a list of tokens associated with a specific user by their ID.

        Parameters:
            user_id (str): The unique identifier of the user whose tokens are to be retrieved.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[TokenV2]: A list of token objects, where each TokenV2 includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional metadata about the token.
                - description (str, optional): A description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the associated user.
        """
        pass



    @raise_for_status_code
    @headers({"Content-Type": "application/json"})
    @json
    @post("api/v1/users/{user_id}/tokens")
    def create_user_token(self, user_id: str, payload: Body(type=TokenRequest),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TokenV2:
        """
        This method creates a new token for a specific user by their ID.

        Parameters:
            user_id (str): The unique identifier of the user for whom the token is to be created.
            payload (Body): The request body containing the token details.
                The TokenRequest object includes:
                - description (str, optional): A human-readable description of the token.
                - duration (str, optional): The duration of the token in ISO 8601 format.
                - name (str, optional): The name of the token.
                - type (str, required): The type of the token.
                - use_existing (bool, optional): Whether to use an existing token if available.
                - user_id (str, optional): The unique identifier of the user associated with the token.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TokenV2: The created token object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional metadata about the token.
                - description (str, optional): A description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the associated user.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/users/{user_id}/tokens/{token_name}")
    def get_user_token(self, user_id: str, token_name: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TokenV2:
        """
        This method retrieves a specific token associated with a user by their ID and the token name.

        Parameters:
            user_id (str): The unique identifier of the user.
            token_name (str): The name of the token to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TokenV2: The retrieved token object, which includes:
                - field_links (Links, optional): Hypermedia links associated with the token.
                - data (Dict[str, str], optional): Additional metadata about the token.
                - description (str, optional): A description of the token.
                - expiration (str, optional): The expiration timestamp of the token.
                - name (str, optional): The name of the token.
                - type (str, optional): The type of the token.
                - user_id (str, optional): The unique identifier of the associated user.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/users/{user_id}/tokens/{token_name}")
    def delete_user_token(self, user_id: str, token_name: str,
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific token associated with a user by their ID and the token name.

        Parameters:
            user_id (str): The unique identifier of the user.
            token_name (str): The name of the token to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass