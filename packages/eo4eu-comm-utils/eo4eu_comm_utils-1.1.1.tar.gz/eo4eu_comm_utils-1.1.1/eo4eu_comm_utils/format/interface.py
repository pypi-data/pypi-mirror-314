from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def fmt(self, input: str) -> str:
        pass
