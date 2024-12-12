from .interface import Comm
from eo4eu_comm_utils.kafka import KafkaProducer


class TopicComm(Comm):
    def __init__(self, producer: KafkaProducer, topic: str, key: str):
        self.producer = producer
        self.topic = topic
        self.key = key

    def send(self, message: str = "", *args, **kwargs):
        self.producer.send_message(
            key = self.key,
            msg = message,
            topic = self.topic
        )
