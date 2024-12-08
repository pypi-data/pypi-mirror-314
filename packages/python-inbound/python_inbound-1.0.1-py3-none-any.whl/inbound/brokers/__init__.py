from urllib.parse import parse_qs, urlparse

from inbound.brokers.base import Broker as Broker
from inbound.brokers.memory import MemoryBroker as MemoryBroker
from inbound.utils import lazy_load_map


_AVAILABLE_BROKERS = {
    "memory": "inbound.brokers.memory.MemoryBroker",
    "amqp": "inbound.brokers.amqp.AMQPBroker",
    "kafka": "inbound.brokers.kafka.KafkaBroker",
}
_AVAILABLE_SERIALIZERS = {
    "msgpack": "inbound.serializers.MsgPackSerializer",
    "json": "inbound.serializers.JSONSerializer",
}


def broker_from_url(url: str, **kwargs) -> Broker:
    """
    Create a Broker instance from a URL.

    :param url: The URL to create the Broker from
    :type url: str
    :return: A Broker instance
    :rtype: Broker
    """
    connection_url = urlparse(url)
    query_params = parse_qs(connection_url.query, keep_blank_values=True)

    broker_cls = lazy_load_map(_AVAILABLE_BROKERS, connection_url.scheme)
    serializer_cls = lazy_load_map(
        _AVAILABLE_SERIALIZERS, query_params.get("serializer", ["json"])[0]
    )

    return broker_cls(url=url, serializer=serializer_cls, **kwargs)


__all__ = ("Broker", "MemoryBroker", "broker_from_url")
