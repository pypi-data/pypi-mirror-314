import uuid
from typing import List

from uplink import *

from commons.http.client.dataos_consumer import DataOSBaseConsumer
from commons.http.client.hadler import raise_for_status_code
from gateway.models.data_policy import DataPolicy

from gateway.models.decision import Decision


class DataPolicyApi(DataOSBaseConsumer):
    @raise_for_status_code
    @returns.json
    @get("api/v1/datapolicy")
    def list(self, correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> List[DataPolicy]:
        pass

    @raise_for_status_code
    @json
    @put("api/v1/datapolicy")
    def create(self, payload: Body(type=DataPolicy),
               correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> None:
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/datapolicy/{name}")
    def get(self, name: str, correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
        pass

    # @raise_for_status_code
    # @returns.json
    # @put("api/v1/datapolicy/{name}")
    # def update(self, name: str, payload: Body(type=DataPolicy),
    #            correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
    #     pass

    @raise_for_status_code
    @returns.json
    @delete("api/v1/datapolicy/{name}")
    def delete(self, name: str, correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> DataPolicy:
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/datapolicy/decision")
    def get_decision(self,
                     depot: Query('depot'),
                     collection: Query('collection'),
                     dataset: Query('dataset'),
                     query_id: Query('queryId') = str(uuid.uuid4()),
                     agent: Query('agent') = None,
                     service_name: Query('serviceName') = None,
                     predicate: Query('predicate') = "read",
                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())
                     ) -> Decision:
        pass

    @raise_for_status_code
    @returns.json
    @get("api/v1/datapolicy/decision/{depot}/{collection}/{dataset}")
    def get_decision_without_context(self, depot: str, collection: str, dataset: str,
                                     query_id: Query('queryId') = str(uuid.uuid4()),
                                     agent: Query('agent') = None,
                                     service_name: Query('serviceName') = None,
                                     predicate: Query('predicate') = "read",
                                     correlation_id: Header("dataos-correlation-id") = str(uuid.uuid4())) -> Decision:
        pass
