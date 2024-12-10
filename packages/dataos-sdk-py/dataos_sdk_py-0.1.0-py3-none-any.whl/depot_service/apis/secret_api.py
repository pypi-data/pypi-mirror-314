from __future__ import absolute_import

import uuid

from typing import Dict
from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from depot_service.models.ds_models import HeimdallSecret


class SecretApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v2/secrets/{secret}")
    def get_secrets(self, secret: str,
                    correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> HeimdallSecret:
        """
        Retrieve a secret from the API.

        This function sends a GET request to fetch a secret with the given name from the API.

        Parameters:
            secret (str): The name of the secret to retrieve.

        Returns:
            HeimdallSecret: An object containing the secrets.
        """
        pass
