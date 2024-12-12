import logging
from importlib.util import find_spec


if find_spec("confluent_kafka") is not None:
    from .producer import KafkaProducer
    from .consumer import KafkaConsumer
else:
    from .unimplemented import KafkaProducer, KafkaConsumer
