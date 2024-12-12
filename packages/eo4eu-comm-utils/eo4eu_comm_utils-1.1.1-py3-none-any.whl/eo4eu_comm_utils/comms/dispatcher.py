from ..compat import Self
from .interface import Comm, LogLevel


class Dispatcher:
    def __init__(
        self,
        comms: dict[str,Comm],
        groups: dict[str,list[str]]|None = None,
        callback = None,
        selection: list[str]|None = None
    ):
        if groups is None:
            groups = {}
        if callback is None:
            callback = lambda this, *args, **kwargs: None

        self._comms = comms
        self._groups = groups
        self._callback = callback
        self._selection = selection

    @classmethod
    def one(cls, comm: Comm, callback = None) -> Self:
        return Dispatcher(
            comms = {"default": comm},
            callback = callback
        )

    @classmethod
    def many(cls, **kwargs) -> Self:
        comms = {}
        groups = {}
        for name, arg in kwargs.items():
            if isinstance(arg, Comm):
                comms[name] = arg
            elif isinstance(arg, list):
                groups[name] = arg

        return Dispatcher(
            comms = comms,
            groups = groups,
        )

    def get_comm(self, name: str) -> Comm:
        return self._comms[name]

    def add_comm(self, name: str, comm: Comm) -> Self:
        self._comms[name] = comm
        return self

    def add_group(self, name: str, sub_names: list[str]) -> Self:
        result = []
        for sub_name in sub_names:
            if sub_name in self._comms:
                result.append(sub_name)
            elif sub_name in self._groups:
                result.extend(self._groups[sub_name])

        self._groups[name] = result
        return self

    def _with_selection(self, selection: list[str]|None) -> Self:
        return Dispatcher(
            comms = self._comms,
            groups = self._groups,
            callback = self._callback,
            selection = selection
        )

    def __getattr__(self, name: str) -> Self:
        if name in self._groups:
            return self._with_selection(self._groups[name])
        if name in self._comms:
            return self._with_selection([name])
        return self._with_selection([])

    def all(self) -> Self:
        return self._with_selection(None)

    def len(self) -> int:
        if self._selection is None:
            return len(self._comms)

        return len(self._selection)

    def send(self, *args, **kwargs):
        self._callback(self, *args, **kwargs)
        selection = self._comms.keys() if self._selection is None else self._selection

        for name in selection:
            self._comms[name].send(*args, **kwargs)

    def add(self, *args, **kwargs):
        self.send(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.send(LogLevel.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self.send(LogLevel.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self.send(LogLevel.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self.send(LogLevel.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self.send(LogLevel.CRITICAL, *args, **kwargs)

    def start(self, *args, **kwargs):
        self.send(LogLevel.START, *args, **kwargs)

    def success(self, *args, **kwargs):
        self.send(LogLevel.SUCCESS, *args, **kwargs)
