import os
import json
from pathlib import Path
from datetime import datetime, timezone

from .interface import Comm, LogLevel
from ..kafka import KafkaProducer


_namespace_path = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")


class MonitoringComm(Comm):
    def __init__(
        self,
        producer: KafkaProducer,
        component_name: str = "Component",
        workflow_name: str|None = None,
        status_dict: dict[LogLevel,str]|None = None,
        **kwargs
    ):
        if workflow_name is None:
            try:
                workflow_name = _namespace_path.read_text()
            except Exception:
                workflow_name = "unknown"

        if status_dict is None:
            status_dict = {
                LogLevel.DEBUG:    "INFO",
                LogLevel.INFO:     "INFO",
                LogLevel.WARNING:  "WARNING",
                LogLevel.ERROR:    "ERROR",
                LogLevel.CRITICAL: "ERROR",
                LogLevel.START:    "START",
                LogLevel.SUCCESS:  "SUCCESS",
            }

        self._producer = producer
        self._workflow_name = workflow_name
        self._component_name = component_name
        self._status_dict = status_dict
        self._kwargs = kwargs
        try:
            self._pod = os.environ["HOSTNAME"]
        except Exception:
            self._pod = "unknown"

    def send(
        self,
        level: LogLevel,
        description: str,
        *args,
        verbose_description: str|None = None,
        **kwargs
    ):
        message = {
            "component_name": self._component_name,
            "workflow_name": self._workflow_name,
            "status": self._status_dict.get(level, "INFO"),
            "description": description,
            "verbose_description": verbose_description,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "optional": {
                "pod": self._pod,
            }
        } | self._kwargs | kwargs

        # trying to be compatible with the different kafka producers
        # floating around
        previous_topic = "monitoring.notify"
        try:
            previous_topic = self._producer._topic
        except Exception:
            pass
        self._producer.set_topic("monitoring.notify")
        self._producer.send_message(
            key = self._component_name,
            msg = json.dumps(message)
        )
        self._producer.set_topic(previous_topic)
