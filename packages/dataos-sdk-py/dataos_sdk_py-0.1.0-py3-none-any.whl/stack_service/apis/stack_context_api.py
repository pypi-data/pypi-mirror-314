from __future__ import absolute_import

from uplink import *
from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from stack_service.models.stack_context import StackContext


class StackContextApi(DataOSBaseConsumer):
    @raise_for_status_code
    @json
    @post("api/v1/publish")
    def publish(self, payload: Body(StackContext)) -> None: pass
