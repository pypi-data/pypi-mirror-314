import uuid

from uplink import *
from typing import List

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import AuthorizationRequest, AuthorizationRequestBatch, UserIdAuthorizationRequest, \
    AuthorizationAtomResponse
from heimdall.models.heimdall_models import AuthorizationResult, AuthorizationResultBatch


class AuthorizeApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @json
    @post("api/v1/authorize")
    def authorize(self, payload: Body(type=AuthorizationRequest),
                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> AuthorizationResult:
        """
        This method authorizes a user action based on the provided payload and correlation ID.

        Parameters:
            payload (Body): The request body containing the details required for authorization.
                The AuthorizationRequest object includes:
                - context (AuthorizationRequestContext, optional): The context for the authorization request,
                  including metadata, object details, and predicate.
                - pep_context (PolicyEnforcementProviderContext, optional): The context related to policy
                  enforcement providers, such as atom ID and user agent.
                - token (str, optional): A token used for authorization purposes.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            AuthorizationResult: The result of the authorization process, which includes:
                - allow (bool, optional): Indicates whether the action is authorized.
                - error (AuthorizationResultError, optional): Contains details of any error that occurred
                  during authorization, including message and status.
                - result (AuthorizationResultData, optional): Contains additional data, such as ID, tags,
                  and other result-related information.
                - valid (bool, optional): Indicates whether the authorization request was valid.
        """
        pass

    @raise_for_status_code
    @returns.json
    @json
    @post("api/v1/authorize/batch")
    def authorize_batch(self, payload: Body(type=AuthorizationRequestBatch),
                        correlation_id: Header("dataos-correlation-id") = str(
                            uuid.uuid4())) -> AuthorizationResultBatch:
        """
        Perform a batch authorization request using the provided payload and correlation ID.

        Parameters:
            payload (Body): The request body containing the details required for batch authorization.
                The AuthorizationRequestBatch object includes:
                - contexts (Dict[str, AuthorizationRequestContext], optional): A dictionary mapping
                  unique identifiers to their respective authorization contexts, including metadata,
                  objects, and predicates.
                - token (str, optional): A token for batch authorization purposes.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            AuthorizationResultBatch: The result of the batch authorization process, which includes:
                - id (str, optional): The unique identifier for the batch authorization request.
                - results (Dict[str, AuthorizationResultBatchSingle], optional): A dictionary mapping
                  unique identifiers to their respective authorization results.
                - tags (List[str], optional): A list of tags associated with the batch authorization.
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @post("api/v1/authorize/user")
    def authorize_user(self, payload: Body(type=UserIdAuthorizationRequest),
                        correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> AuthorizationResult:
        """
        This method authorizes a user action based on their user ID.

        Parameters:
            payload (Body): The request body containing the details required for user authorization.
                The UserIdAuthorizationRequest object includes:
                - context (AuthorizationRequestContext, optional): The context for the authorization request, 
                  including metadata, object details, and predicate.
                - pep_context (PolicyEnforcementProviderContext, optional): The context related to policy 
                  enforcement providers, such as atom ID and user agent.
                - user_id (str, optional): The unique identifier of the user requesting authorization.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            AuthorizationResult: The result of the authorization process, which includes:
                - allow (bool, optional): Indicates whether the action is authorized.
                - error (AuthorizationResultError, optional): Contains details of any error that occurred 
                  during authorization, including message and status.
                - result (AuthorizationResultData, optional): Contains additional data, such as ID, tags, 
                  and other result-related information.
                - valid (bool, optional): Indicates whether the authorization request was valid.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/atoms")
    def list_authorization_atoms(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[AuthorizationAtomResponse]:
        """
        This method retrieves a list of all authorization atoms.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[AuthorizationAtomResponse]: A list of authorization atom objects, which include:
                - id (str, optional): The unique identifier of the authorization atom.
                - description (str, optional): A human-readable description of the atom.
                - predicate (str, optional): The condition or rule associated with the atom.
                - tags (List[str], optional): Tags linked to the authorization atom.
                - conditions (List[PolicyConditions], optional): The conditions under which the atom applies.
                - policy_enforcement_provider_id (str, optional): The ID of the associated policy enforcement provider.
                - variables (List[str], optional): Variables required for the atom's evaluation.
                - created_at (str, optional): The timestamp when the atom was created.
                - updated_at (str, optional): The timestamp when the atom was last updated.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/atoms/{id}")
    def get_authorization_atom(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> AuthorizationAtomResponse:
        """
        This method retrieves the details of a specific authorization atom by its ID.

        Parameters:
            id (str): The unique identifier of the authorization atom to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            AuthorizationAtomResponse: The details of the specified authorization atom, which include:
                - id (str, optional): The unique identifier of the authorization atom.
                - description (str, optional): A human-readable description of the atom.
                - predicate (str, optional): The condition or rule associated with the atom.
                - tags (List[str], optional): Tags linked to the authorization atom.
                - conditions (List[PolicyConditions], optional): The conditions under which the atom applies.
                - policy_enforcement_provider_id (str, optional): The ID of the associated policy enforcement provider.
                - variables (List[str], optional): Variables required for the atom's evaluation.
                - created_at (str, optional): The timestamp when the atom was created.
                - updated_at (str, optional): The timestamp when the atom was last updated.
        """
        pass