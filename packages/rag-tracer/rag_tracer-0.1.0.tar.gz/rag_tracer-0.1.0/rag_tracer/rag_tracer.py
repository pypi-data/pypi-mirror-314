import requests


class RAGTracer:

    _TEST_URL = "http://101.42.184.25:8095/api/tracer"

    def __init__(self, server_url):
        self.server_url = server_url

    def send_trace(self, trace_data):
        response = requests.post(f"{self._TEST_URL}/publish", json=trace_data)
        return response.json()
