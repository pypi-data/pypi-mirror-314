import uuid

from uplink import Header, get, returns, post, delete, Body, headers, Query
from typing import List
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import PolicyUseCaseGrantRequest, PolicyUseCaseGrantResponse,\
    PolicyUseCaseGrantRequestDB, PolicyUseCaseGrant


class PolicyUseCaseGrantRequestsApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/grant-requests")
    def list_grant_requests(self, use_case_id: Query('use_case_id') = None,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[PolicyUseCaseGrantRequestDB]:
        """
        This method retrieves a list of all policy use case grant requests.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[PolicyUseCaseGrantRequestDB]: A list of grant request objects, where each object includes:
                - collection (str, optional): The collection to which the grant request belongs.
                - creator (str, optional): The user who created the grant request.
                - decision (str, optional): The decision status of the grant request.
                - id (str, optional): The unique identifier of the grant request.
                - notes (str, optional): Additional notes related to the grant request.
                - policy_use_case_grant_id (str, optional): The ID of the associated policy use case grant.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - requester (str, optional): The user who made the grant request.
                - source (str, optional): The source of the grant request.
                - state (str, optional): The current state of the grant request.
                - subjects (List[str], optional): The subjects involved in the grant request.
                - values (MapMapSliceValues, optional): Associated values for the grant request.
        """
        pass

    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/grant-requests")
    def create_grant_request(self, payload: Body(type=PolicyUseCaseGrantRequest),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrantResponse:
        """
        This method creates a new policy use case grant request.

        Parameters:
            payload (Body): The request body containing the details of the grant request to be created.
                The PolicyUseCaseGrantRequest object includes:
                - collection (str, optional): The collection to which the grant request belongs.
                - notes (str, optional): Additional notes related to the grant request.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - requester (str, optional): The user who made the grant request.
                - source (str, optional): The source of the grant request.
                - subjects (List[str], optional): The subjects involved in the grant request.
                - values (MapMapSliceValues, optional): Associated values for the grant request.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrantResponse: The created grant request object, which includes:
                - id (str, optional): The unique identifier of the grant request.
                - collection (str, optional): The collection to which the grant request belongs.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - subjects (List[str], optional): The subjects involved in the grant request.
                - policies (List[PolicyPersistence], optional): A list of associated policies.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values for the grant request.
                - created_at (str, optional): The timestamp when the grant request was created.
                - updated_at (str, optional): The timestamp when the grant request was last updated.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/grant-requests/{id}")
    def get_grant_request(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrantRequestDB:
        """
        This method retrieves the details of a specific policy use case grant request by its ID.

        Parameters:
            id (str): The unique identifier of the grant request to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrantRequestDB: The details of the specified grant request, which includes:
                - collection (str, optional): The collection to which the grant request belongs.
                - creator (str, optional): The user who created the grant request.
                - decision (str, optional): The decision status of the grant request.
                - id (str, optional): The unique identifier of the grant request.
                - notes (str, optional): Additional notes related to the grant request.
                - policy_use_case_grant_id (str, optional): The ID of the associated policy use case grant.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - requester (str, optional): The user who made the grant request.
                - source (str, optional): The source of the grant request.
                - state (str, optional): The current state of the grant request.
                - subjects (List[str], optional): The subjects involved in the grant request.
                - values (MapMapSliceValues, optional): Associated values for the grant request.
        """
        pass


    @raise_for_status_code
    @delete("api/v1/grant-requests/{id}")
    def delete_grant_request(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific policy use case grant request by its ID.

        Parameters:
            id (str): The unique identifier of the grant request to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass

    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/grant-requests/{id}/approve")
    def approve_grant_request(self, id: str,
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrant:
        """
        This method approves a specific policy use case grant request by its ID.

        Parameters:
            id (str): The unique identifier of the grant request to approve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrant: The approved grant object, which includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policies (List[PolicyPersistence], optional): A list of associated policies.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values for the grant.
        """
        pass

    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/grant-requests/{id}/reject")
    def reject_grant_request(self, id: str,
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrant:
        """
        This method rejects a specific policy use case grant request by its ID.

        Parameters:
            id (str): The unique identifier of the grant request to reject.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrant: The rejected grant object, which includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policies (List[PolicyPersistence], optional): A list of associated policies.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values for the grant.
        """
        pass