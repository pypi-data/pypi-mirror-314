from ..compat import _get_import_error


class KafkaProducer:
    def __init__(self, *args, **kwargs):
        raise ImportError(_get_import_error("KafkaProducer", "kafka"))


class KafkaConsumer:
    def __init__(self, *args, **kwargs):
        raise ImportError(_get_import_error("KafkaConsumer", "kafka"))
