from .interface import Comm

class DummyComm(Comm):
    def send(*args, **kwargs):
        pass
