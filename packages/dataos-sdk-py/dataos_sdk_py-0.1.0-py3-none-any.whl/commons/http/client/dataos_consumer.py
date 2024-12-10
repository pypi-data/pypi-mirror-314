from uplink import *


class DataOSBaseConsumer(Consumer):
    def __init__(self,  base_url, apikey, client=None):
        super().__init__(base_url=base_url, client=client)
        self._inject(Header("apikey").with_value(apikey))
