import uuid

from typing import List

from uplink import Header, get, returns, post, delete, Body, headers, Query, json

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from heimdall.models.heimdall_models import UserTagsRequest, TagGroup, TagNamespace, TagResponse


class TagsApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v1/tags")
    def list_tags(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[str]:
        """
        This method retrieves a list of all tags.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[str]: A list of tag labels, where each label represents the name or identifier of a tag.
        """
        pass


    @raise_for_status_code
    @returns.json
    @json
    @headers({"Content-Type": "application/json"})
    @post("api/v1/tags")
    def upsert_user_tags(self, payload: Body(type=UserTagsRequest),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> UserTagsRequest:
        """
        This method creates or updates tags for a user.

        Parameters:
            payload (Body): The request body containing the details of the user and tags to be created or updated.
                The UserTagsRequest object includes:
                - tags (List[str], optional): A list of tags to associate with the user.
                - user_id (str, optional): The unique identifier of the user to associate the tags with.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            UserTagsRequest: The object containing the updated tags and user information, which includes:
                - tags (List[str], optional): The updated list of tags associated with the user.
                - user_id (str, optional): The unique identifier of the user associated with the tags.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/tags/{user_id}")
    def get_user_tags(self, user_id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> UserTagsRequest:
        """
        This method retrieves the tags associated with a specific user.

        Parameters:
            user_id (str): The unique identifier of the user whose tags are to be retrieved.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            UserTagsRequest: An object containing the tags associated with the user, which includes:
                - tags (List[str], optional): The list of tags associated with the user.
                - user_id (str, optional): The unique identifier of the user associated with the tags.
        """
        pass


    @raise_for_status_code
    @delete("api/v1/tags/{user_id}")
    def delete_user_tags(self, user_id: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes all tags associated with a specific user.

        Parameters:
            user_id (str): The unique identifier of the user whose tags are to be deleted.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass


    @raise_for_status_code
    @delete("api/v1/tags/{user_id}/tag/{tag}")
    def delete_specific_user_tag(self, user_id: str, tag: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> UserTagsRequest:
        """
        This method deletes a specific tag associated with a user by their ID and tag name.

        Parameters:
            user_id (str): The unique identifier of the user whose tag is to be deleted.
            tag (str): The specific tag to be deleted from the user's tags.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            UserTagsRequest: An object containing the updated list of tags for the user, which includes:
                - tags (List[str], optional): The updated list of tags associated with the user after the deletion.
                - user_id (str, optional): The unique identifier of the user associated with the updated tags.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/tag-groups")
    def list_tag_groups(self, tag: Query('tag') = None,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[TagGroup]:
        """
        This method retrieves a list of tag groups, optionally filtered by a specific tag.

        Parameters:
            tag (str, optional): A query parameter to filter tag groups by a specific tag.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[TagGroup]: A list of tag group objects, where each TagGroup includes:
                - name (str, optional): The name of the tag group.
                - tags (List[Tag], optional): A list of tag objects associated with the group, where each Tag includes:
                    - label (str, optional): The label or name of the tag.
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/tag-namespaces")
    def list_tag_namespaces(self,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[TagNamespace]:
        """
        This method retrieves a list of all tag namespaces.

        Parameters:
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[TagNamespace]: A list of tag namespace objects, where each TagNamespace includes:
                - name (str, optional): The name of the tag namespace.
                - description (str, optional): A human-readable description of the tag namespace.
                - type (str, optional): The type of the tag namespace.
                - glob (str, optional): A glob pattern representing the tag namespace's structure.
        """
        pass


    @raise_for_status_code
    @returns.json
    @headers({"Content-Type": "application/json"})
    @post(f"api/v1/tag-namespaces")
    def create_tag_namespace(self, payload: Body(type=TagNamespace),
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TagNamespace:
        """
        This method creates a new tag namespace.

        Parameters:
            payload (Body): The request body containing the details of the tag namespace to be created.
                The TagNamespace object includes:
                - name (str, optional): The name of the tag namespace.
                - description (str, optional): A human-readable description of the tag namespace.
                - type (str, optional): The type of the tag namespace.
                - glob (str, optional): A glob pattern representing the structure of the tag namespace.

            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TagNamespace: The created tag namespace object, which includes:
                - name (str, optional): The name of the tag namespace.
                - description (str, optional): A human-readable description of the tag namespace.
                - type (str, optional): The type of the tag namespace.
                - glob (str, optional): A glob pattern representing the structure of the tag namespace.
        """
        pass


    @raise_for_status_code
    @delete("api/v1/tag-namespaces/{name}")
    def delete_tag_namespace(self, name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        This method deletes a specific tag namespace by its name.

        Parameters:
            name (str): The name of the tag namespace to delete.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            None
        """
        pass


    @raise_for_status_code
    @returns.json
    @get("api/v1/tag-namespaces/{name}")
    def get_tag_namespace(self, name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> TagNamespace:
        """
        This method retrieves the details of a specific tag namespace by its name.

        Parameters:
            name (str): The name of the tag namespace to retrieve.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            TagNamespace: The details of the specified tag namespace, which includes:
                - name (str, optional): The name of the tag namespace.
                - description (str, optional): A human-readable description of the tag namespace.
                - type (str, optional): The type of the tag namespace.
                - glob (str, optional): A glob pattern representing the structure of the tag namespace.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/tag-namespaces/{name}/tags")
    def get_tags_within_namespace(self, name: str,
             correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[TagResponse]:
        """
        This method retrieves all tags within a specific tag namespace.

        Parameters:
            name (str): The name of the tag namespace for which to retrieve tags.
            correlation_id (str, optional): The correlation ID used for tracking and logging the request.
                Defaults to a new UUID (Universally Unique Identifier) generated using the uuid.uuid4() method.

        Returns:
            List[TagResponse]: A list of tag response objects, where each TagResponse includes:
                - label (str, optional): The label or name of the tag.
                - type (str, optional): The type of the tag (e.g., namespace or other category).
        """
        pass
