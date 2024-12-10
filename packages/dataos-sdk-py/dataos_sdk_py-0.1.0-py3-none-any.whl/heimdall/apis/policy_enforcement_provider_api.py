import uuid

from typing import List

from uplink import Header, get, returns, delete, Body, headers, post

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import PolicyEnforcementProviderThinResponse, PolicyEnforcementProvider, \
PolicyEnforcementProviderResponse


class PolicyEnforcementProviderApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/providers")
    def list_providers(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[PolicyEnforcementProviderThinResponse]:
        """
        This method retrieves a list of all policy enforcement providers.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[PolicyEnforcementProviderThinResponse]: A list of policy enforcement provider objects, where each object includes:
                - id (str, optional): The unique identifier of the policy enforcement provider.
                - name (str, optional): The name of the policy enforcement provider.
                - description (str, optional): A human-readable description of the provider.
                - version (str, optional): The version of the policy enforcement provider.
                - created_at (str, optional): The timestamp when the provider was created.
                - updated_at (str, optional): The timestamp when the provider was last updated.
                - field_links (Links, optional): Links associated with the provider for navigation.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/providers/{id}")
    def get_provider(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyEnforcementProviderResponse:
        """
        This method retrieves the details of a specific policy enforcement provider by its ID.

        Parameters:
            id (str): The unique identifier of the policy enforcement provider to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyEnforcementProviderResponse: The details of the specified policy enforcement provider, which include:
                - id (str, optional): The unique identifier of the policy enforcement provider.
                - name (str, optional): The name of the policy enforcement provider.
                - description (str, optional): A human-readable description of the provider.
                - version (str, optional): The version of the policy enforcement provider.
                - created_at (str, optional): The timestamp when the provider was created.
                - updated_at (str, optional): The timestamp when the provider was last updated.
                - authorization_atoms (List[AuthorizationAtom], optional): A list of associated authorization atoms.
                - field_links (Links, optional): Links associated with the provider for navigation.
        """

        pass

    @raise_for_status_code
    @delete("api/v1/providers/{id}")
    def delete_provider(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific policy enforcement provider by its ID.

        Parameters:
            id (str): The unique identifier of the policy enforcement provider to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """

        pass

    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/policy-provider")
    def create_policy_provider(self, payload: Body(type=PolicyEnforcementProvider),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyEnforcementProvider:
        """
        This method creates a new policy enforcement provider.

        Parameters:
            payload (Body): The request body containing the details of the policy enforcement provider to be created.
                The PolicyEnforcementProvider object includes:
                - id (str, optional): The unique identifier of the policy enforcement provider.
                - name (str, optional): The name of the policy enforcement provider.
                - description (str, optional): A human-readable description of the provider.
                - version (str, optional): The version of the policy enforcement provider.
                - authorization_atoms (List[AuthorizationAtom], optional): A list of associated authorization atoms.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyEnforcementProvider: The created policy enforcement provider object, which includes:
                - id (str, optional): The unique identifier of the policy enforcement provider.
                - name (str, optional): The name of the policy enforcement provider.
                - description (str, optional): A human-readable description of the provider.
                - version (str, optional): The version of the policy enforcement provider.
                - authorization_atoms (List[AuthorizationAtom], optional): A list of associated authorization atoms.
        """

        pass