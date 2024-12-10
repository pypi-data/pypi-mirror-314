from skywalking.trace.context import get_context

from client.rag_tracer.node_info import NodeInfo
from client.rag_tracer.trace_client import TraceClient


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

    def publish(self, node_key, data_dict):
        """
        一键发布事件
        :param node_key:
        :param data_dict:
        :return:
        """
        node = self.build_node(node_key)
        node.event_data(data_dict)
        self.publish_node(node)
