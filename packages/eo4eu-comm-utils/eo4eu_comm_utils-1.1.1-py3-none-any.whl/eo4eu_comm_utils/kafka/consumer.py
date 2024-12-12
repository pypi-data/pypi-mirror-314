from logging import Logger
from confluent_kafka import Consumer, Message

from .log import default_logger
from ..compat import Callable


class KafkaConsumer:
    def __init__(
        self,
        topics: list[str]|str,
        config: dict,
        handler: Callable[[str],None]|None = None,
        logger: Logger|None = None,
        timeout: float = 1.0,
        callback: Callable[[Message,str],None]|None = None
    ):
        if not isinstance(topics, list):
            topics = [topics]
        if logger is None:
            logger = default_logger
        if callback is None:
            callback = lambda msg, dec_msg: logger.info(
                f"[Topic {msg.topic()}] Message received: {dec_msg}"
            )

        self._consumer = Consumer(config)
        self._topics = topics
        self._handler = handler
        self._logger = logger
        self._timeout = timeout
        self._callback = callback

    def consume(self, handler: Callable[[str],None]|None = None):
        if handler is None:
            handler = self._handler

        try:
            self._consumer.subscribe(self._topics)
            while True:
                msg = self._consumer.poll(timeout = self._timeout)
                if msg is None or msg.error():
                    continue

                decoded_msg = msg.value().decode("utf-8")
                self._callback(msg, decoded_msg)
                handler(decoded_msg)
        finally:
            self._consumer.close()
