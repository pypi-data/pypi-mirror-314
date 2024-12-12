from logging import Logger
from functools import partial
from confluent_kafka import Producer

from .log import default_logger
from ..compat import Self


def _default_callback(err, msg, logger):
    if err is not None:
        logger.error(
            f"[Topic {msg.topic()}] Failed to deliver message: {str(msg.value())}: {str(err)}"
        )
    else:
        logger.info(
            f"[Topic {msg.topic()}] Message produced: {str(msg.value())}"
        )


class KafkaProducer:
    def __init__(
        self,
        topic: str,
        config: dict,
        logger: Logger|None = None,
        callback = None
    ):
        if logger is None:
            logger = default_logger
        if callback is None:
            callback = partial(_default_callback, logger = logger)

        self._topic = topic
        self._logger = logger
        self._producer = Producer(config)
        self._callback = callback

    @classmethod
    def from_config(cls, config: dict, **kwargs) -> Self:
        return KafkaProducer(None, config, **kwargs)

    def set_topic(self, topic: str):
        self._topic = topic

    def send_message(self, key: str, msg: str, topic: str|None = None, callback = None):
        if topic is None:
            topic = self._topic
        if callback is None:
            callback = self._callback

        self._producer.produce(topic, key=key, value=msg, callback=callback)
        self._producer.flush()
