class NodeInfo:
    def __init__(self, trace_id, node_key):
        self._trace_id = trace_id
        self._node_key = node_key
        self._event_data = {}

        # 其他系统字段
        self._endpoint = '__default_endpoint__'
        self._time_cost = -1

    def set(self, **kwargs):
        for key, value in kwargs.items():
            self._event_data[key] = value

    def endpoint(self, endpoint):
        self._endpoint = endpoint

    def time_cost(self, time_cost):
        self._time_cost = time_cost

    def event_data(self, event_data):
        self._event_data = event_data

    def to_dict(self):
        return {
            "trace_id": self._trace_id,
            "endpoint": self._endpoint,
            "node_key": self._node_key,
            "event_data": self._event_data,
            "time_cost": self._time_cost
        }
