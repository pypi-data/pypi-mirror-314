import uuid

from typing import List
from uplink import Header, get, returns, post, put, delete, Body

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import Policy, PolicyList


class PolicyApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v1/policies")
    def list_policies(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[Policy]:
        """
        This method retrieves a list of all policies.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[Policy]: A list of policy objects, which include:
                - name (str, optional): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.
        """
        pass

    @raise_for_status_code
    @returns.json
    @post("api/v1/policies")
    def create_policy(self, payload: Body(type=Policy),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Policy:
        """
        This method creates a new policy.

        Parameters:
            payload (Body): The request body containing the details of the policy to be created.
                The Policy object includes:
                - name (str, optional): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Policy: The created policy object, which includes:
                - name (str): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/policies/{name}")
    def get_policy(self, name: str,
            correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Policy:
        """
        This method retrieves the details of a specific policy by its name.

        Parameters:
            name (str): The unique identifier of the policy to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Policy: The details of the specified policy, which includes:
                - name (str): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.
        """
        pass

    @raise_for_status_code
    @returns.json
    @put("api/v1/policies/{name}")
    def update_policy(self, name: str, payload: Body(type=Policy),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Policy:
        """
        This method updates the details of a specific policy by its name.

        Parameters:
            name (str): The unique identifier of the policy to update.
            payload (Body): The request body containing the updated details of the policy.
                The Policy object includes:
                - name (str, optional): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            Policy: The updated policy object, which includes:
                - name (str): The unique identifier of the policy.
                - description (str, optional): A human-readable description of the policy.
                - allow (bool, optional): Indicates whether the policy allows or denies access.
                - collection (str, optional): The collection to which the policy belongs.
                - conditions (List[PolicyConditions], optional): The conditions under which the policy is active.
                - predicates (List[str], optional): The actions to which the policy applies.
                - objects (Objects, optional): The targets (paths or tags) to which the policy applies.
                - subjects (Subjects, optional): The subjects (tags or groups) to which the policy applies.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/policies/{name}")
    def delete_policy(self, name: str,
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific policy by its name.

        Parameters:
            name (str): The unique identifier of the policy to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v2/policies")
    def list_policies_v2(self,
                correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> PolicyList:
        """
        This method retrieves a list of policies in the v2 format.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            PolicyList: A paginated list of policy objects in the v2 format, which includes:
                - page (int, optional): The current page number.
                - size (int, optional): The number of policies per page.
                - total_pages (int, optional): The total number of pages available.
                - total_records (int, optional): The total number of policy records.
                - policies (List[PolicyThinResponse], optional): A list of policies, where each PolicyThinResponse includes:
                    - name (str, optional): The unique identifier of the policy.
                    - description (str, optional): A human-readable description of the policy.
                    - collection (str, optional): The collection to which the policy belongs.
                    - field_links (Links, optional): Links associated with the policy for navigation.
        """
        pass
