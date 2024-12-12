import traceback
import logging
from .interface import Comm, LogLevel


class LogComm(Comm):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def send(self, level: LogLevel, msg: str = "", *args, **kwargs):
        self.logger.log(level.to_logging_level(), msg)
