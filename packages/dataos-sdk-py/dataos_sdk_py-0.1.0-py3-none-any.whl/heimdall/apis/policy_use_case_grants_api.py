import uuid

from typing import List

from uplink import Header, get, returns, post, put, delete, Body, headers

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import  PolicyUseCaseGrantThinResponse, \
    PolicyUseCaseGrantRequest, PolicyUseCaseGrantResponse, Change


class PolicyUseCaseGrantsApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v1/grants")
    def list_grants(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[PolicyUseCaseGrantThinResponse]:
        """
        This method retrieves a list of all policy use case grants.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[PolicyUseCaseGrantThinResponse]: A list of policy use case grant objects, where each object includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values for the grant.
                - field_links (Links, optional): Links associated with the grant for navigation.
                - created_at (str, optional): The timestamp when the grant was created.
                - updated_at (str, optional): The timestamp when the grant was last updated.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/grants")
    def create_grant(self, payload: Body(type=PolicyUseCaseGrantRequest),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrantResponse:
        """
        This method creates a new policy use case grant.

        Parameters:
            payload (Body): The request body containing the details of the grant to be created.
                The PolicyUseCaseGrantRequest object includes:
                - collection (str, optional): The collection to which the grant belongs.
                - notes (str, optional): Additional notes related to the grant.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - requester (str, optional): The user who made the grant request.
                - source (str, optional): The source of the grant request.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (MapMapSliceValues, optional): Associated values for the grant.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrantResponse: The created grant object, which includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - policies (List[PolicyPersistence], optional): A list of associated policies, where each PolicyPersistence includes:
                    - id (str, optional): The unique identifier of the policy.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters, represented as key-value pairs.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values, where each AuthorizationAtomValues includes:
                    - authorization_atom_id (str, optional): The ID of the authorization atom.
                    - variable_values (List[Dict[str, str]], optional): Key-value pairs for the authorization atom variables.
                - created_at (str, optional): The timestamp when the grant was created.
                - updated_at (str, optional): The timestamp when the grant was last updated.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/grants/{id}")
    def get_grant(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyUseCaseGrantResponse:
        """
        This method retrieves the details of a specific policy use case grant by its ID.

        Parameters:
            id (str): The unique identifier of the grant to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyUseCaseGrantResponse: The details of the specified grant, which includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - policies (List[PolicyPersistence], optional): A list of associated policies, where each PolicyPersistence includes:
                    - id (str, optional): The unique identifier of the policy.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters, represented as key-value pairs.
                - subjects (List[str], optional): The subjects involved in the grant.
                - values (List[AuthorizationAtomValues], optional): Authorization atom values, where each AuthorizationAtomValues includes:
                    - authorization_atom_id (str, optional): The ID of the authorization atom.
                    - variable_values (List[Dict[str, str]], optional): Key-value pairs for the authorization atom variables.
                - created_at (str, optional): The timestamp when the grant was created.
                - updated_at (str, optional): The timestamp when the grant was last updated.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/grants/{id}")
    def delete_grant(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific policy use case grant by its ID.

        Parameters:
            id (str): The unique identifier of the grant to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/grants/{id}/changes")
    def get_grant_changes(self, id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Change]:
        """
        This method retrieves a list of changes associated with a specific policy use case grant.

        Parameters:
            id (str): The unique identifier of the grant to get changes for.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Change]: A list of changes associated with the grant, where each Change includes:
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
    @delete("api/v1/grants/{id}/tags/{tag}")
    def delete_grant_tag(self, id: str, tag: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific tag from a policy use case grant by its ID and tag name.

        Parameters:
            id (str): The unique identifier of the grant.
            tag (str): The name of the tag to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/grants/subjects/{tag}")
    def list_grants_by_subject(self, tag: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[PolicyUseCaseGrantThinResponse]:
        """
        This method retrieves a list of grants associated with a specific subject tag.

        Parameters:
            tag (str): The subject tag to filter grants by.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[PolicyUseCaseGrantThinResponse]: A list of grants associated with the specified subject tag, where each grant includes:
                - id (str, optional): The unique identifier of the grant.
                - collection (str, optional): The collection to which the grant belongs.
                - policy_use_case_id (str, optional): The ID of the associated policy use case.
                - subjectGranters (MapValues, optional): A mapping of subjects to granters.
                - subjects (List[str], optional): The subjects involved in the grant.
                - field_links (Links, optional): Links associated with the grant for navigation.
                - created_at (str, optional): The timestamp when the grant was created.
                - updated_at (str, optional): The timestamp when the grant was last updated.
        """
        pass
