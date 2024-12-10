from __future__ import absolute_import

import uuid
from typing import List

from uplink import *

from asset_tags_service.models.asset_tag_assign_request import AssetTagAssignRequest
from asset_tags_service.models.asset_tag_group import AssetTagGroup
from asset_tags_service.models.asset_tags import AssetTags
from asset_tags_service.models.bulk_asset_tag_request import BulkAssetTagRequest
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code


class AssetTagsApi(DataOSBaseConsumer):
    @raise_for_status_code
    @json
    @put("api/v1/asset-tags")
    def assign_tag_to_asset(self, payload: Body(AssetTagAssignRequest),
                            correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Assigns a tag to an asset.

        Parameters:
            correlation_id (str): The correlation ID for tracking the request (sent as a header).
            payload (AssetTagAssignRequest): An instance of AssetTagAssignRequest containing the information
                about the tag and asset (sent as the request body).

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @json
    @put("api/v1/asset-tags/bulk")
    def assign_and_remove_in_bulk(self, payload: Body(BulkAssetTagRequest),
                                  correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        """
        Assigns and removes asset tags in bulk.

        This method sends a PUT request to the endpoint 'api/v1/asset-tags/bulk'
        with the provided correlation ID and payload as the request body.

        Parameters:
            payload (BulkAssetTagRequest): An instance of BulkAssetTagRequest
                containing the information about the asset tags to be assigned and removed.

        Returns:
            None: This method does not return anything.
        """
        pass

    @raise_for_status_code
    @delete("api/v1/asset-tags")
    def delete_tag_asset_mapping(self, assetFqn: Query('assetFqn'), tagFqn: Query('tagFqn'),
                                 correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())):
        """
        Deletes the mapping between a tag and an asset.

        This method sends a DELETE request to the endpoint 'api/v1/asset-tags' to delete
        the mapping between the specified assetFqn and tagFqdn.

        Parameters:
            correlation_id (str): The correlation ID for tracking the request (sent as a header).
            assetFqn (str): The fully qualified name of the asset whose mapping is to be deleted (sent as a query parameter).
            tagFqdn (str): The fully qualified name of the tag whose mapping is to be deleted (sent as a query parameter).

        Returns:
            List[AssetTagGroup]: A list of AssetTagGroup objects representing the remaining mappings
                between assets and tags after deletion.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/asset-tags")
    def get_asset_tags_by_asset_fqn(self, assetFqn: Query('assetFqn'),
                                    correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> \
            List[AssetTagGroup]:
        """
        Get asset tags associated with a specific asset.

        This method sends a GET request to the endpoint 'api/v1/asset-tags' with the provided
        correlation ID and assetFqn as query parameters to retrieve asset tags associated
        with the specified asset.

        Parameters:
            correlation_id (str): The correlation ID for tracking the request (sent as a header).
            assetFqn (str): The fully qualified name of the asset to retrieve asset tags for (sent as a query parameter).

        Returns:
            List[AssetTagGroup]: A list of AssetTagGroup objects representing the mappings between the asset and tags.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/asset-tags")
    def get_asset_tags_by_group_id(self, groupId: Query('groupId'),
                                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> \
            List[AssetTagGroup]:
        """
        Get asset tags associated with a specific group.

        This method sends a GET request to the endpoint 'api/v1/asset-tags' with the provided
        correlation ID and group_id as query parameters to retrieve asset tags associated
        with the specified group.

        Parameters:
            correlation_id (str): The correlation ID for tracking the request (sent as a header).
            groupId (str): The ID of the group to retrieve asset tags for (sent as a query parameter).

        Returns:
            List[AssetTagGroup]: A list of AssetTagGroup objects representing the mappings between the assets and tags in the group.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/asset-tags?group=false")
    def get_asset_tags(self, groupId: Query('groupId'),
                       correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[AssetTags]:
        """
        Get asset tags.

        This method sends a GET request to the endpoint 'api/v1/asset-tags?group=false' with the provided
        correlation ID and group_id as query parameters to retrieve asset tags.

        Parameters:
            correlation_id (str): The correlation ID for tracking the request (sent as a header).
            groupId (str): The ID of the group to filter asset tags (sent as a query parameter).

        Returns:
            List[AssetTags]: A list of AssetTags objects representing the asset tags.
        """
        pass
