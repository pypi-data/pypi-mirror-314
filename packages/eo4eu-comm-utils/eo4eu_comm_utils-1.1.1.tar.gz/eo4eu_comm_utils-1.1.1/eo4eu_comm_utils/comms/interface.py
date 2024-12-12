import logging
from abc import ABC, abstractmethod
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    START = 0
    SUCCESS = 1

    def to_logging_level(self) -> int:
        if self in {LogLevel.START, LogLevel.SUCCESS}:
            return logging.INFO

        return self.value


class Comm(ABC):
    @abstractmethod
    def send(*args, **kwargs):
        pass
