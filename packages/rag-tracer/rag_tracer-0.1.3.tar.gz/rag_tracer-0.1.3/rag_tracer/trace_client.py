import requests


class TraceClient:
    _TEST_URL = "http://xyz.rag-workflow.test.ke.com/api/tracer"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def publish(self, trace_data):
        response = requests.post(f"{self._TEST_URL}/publish", json=trace_data)
        return response.json()
