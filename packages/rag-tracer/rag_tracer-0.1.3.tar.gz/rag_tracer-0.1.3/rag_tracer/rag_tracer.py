from skywalking.trace.context import get_context

from rag_tracer.node_info import NodeInfo
from rag_tracer.trace_client import TraceClient


class RAGTracer:

    def __init__(self, trace_id='__broken_trace_id__'):
        self._trace_id = trace_id
        self._api_key = '__public_api_key__'
        self._trace_client = TraceClient.instance()

    @classmethod
    def instance(cls, trace_id=None):
        if not trace_id:
            trace_id = cls._get_skywalking_trace_id()
        return cls(trace_id)

    @staticmethod
    def _get_skywalking_trace_id():
        context = get_context()
        trace_id = context.segment.related_traces[0].value
        return trace_id

    def build_node(self, node_key):
        """
        构建节点, 搭配 publish_node 使用
        :param node_key:
        :return:
        """
        node = NodeInfo(self._trace_id, node_key)
        return node

    def publish_node(self, node):
        """
        发布节点, 搭配 build_node 使用
        :param node:
        :return:
        """
        self._trace_client.publish(node.to_dict())

    def event_publish(self, node_key, event_data):
        """
        一键发布事件
        :param node_key:
        :param event_data:
        :return:
        """
        node = self.build_node(node_key)
        node.event_data(event_data)
        self.publish_node(node)

    def kv_publish(self, node_key, **kwargs):
        """
        一键发布事件(动态参数)
        :param node_key:
        :param kwargs:
        :return:
        """
        node = self.build_node(node_key)
        node.set(**kwargs)
        self.publish_node(node)

    def builder(self, node_key):
        """
        一键发布事件(链式调用)
        :param node_key:
        :return:
        """
        return self.Builder(node_key, self._trace_id, self._trace_client)

    class Builder:
        def __init__(self, node_key, trace_id, trace_client):
            self._trace_client = trace_client
            self._node = NodeInfo(trace_id, node_key)

        def fill(self, **kwargs):
            for key, value in kwargs.items():
                self._node.set(key, value)
            return self

        def flush(self):
            self._trace_client.publish(self._node.to_dict())
