from __future__ import absolute_import

import uuid

from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from depot_service.models.ds_models import AddressInfo, ResolverResponse


class ResolveApi(DataOSBaseConsumer):

    @raise_for_status_code
    @returns.json
    @get("api/v2/tenants/{tenant}/resolve")
    def resolve(self, tenant: str, address: Query('address'),
                correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> AddressInfo:
        """
        Resolve an address to obtain address information.

        This function sends a GET request to resolve the provided address and retrieve address information.

        Parameters:
            tenant (str): The name of the tenant.
            address (str): The address to be resolved.

        Returns:
            AddressInfo: An object representing the address information.
                The object may contain various properties such as street address, city, state, postal code, etc.
        """
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v3/tenants/{tenant}/resolve")
    def resolve_v3(self, tenant: str, address: Query('address'),
                   correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> ResolverResponse:
        """
        Resolve an address to obtain address information.

        This function sends a GET request to resolve the provided address and retrieve address information.

        Parameters:
            tenant (str): The name of the tenant.
            address (str): The address to be resolved.

        Returns:
            ResolverResponse: An object representing the address information.
                The object may contain various properties such as street address, city, state, postal code, etc.
        """
        pass
