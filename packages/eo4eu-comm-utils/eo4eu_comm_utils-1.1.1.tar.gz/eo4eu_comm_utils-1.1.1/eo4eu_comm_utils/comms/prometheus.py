from enum import Enum
from importlib.util import find_spec

from .interface import Comm
from ..compat import _get_import_error


if find_spec("prometheus_client") is not None:
    from prometheus_client import Counter, Gauge, start_http_server

    class CounterComm(Comm):
        def __init__(self, counter: Counter):
            self._counter = counter

        def send(self, value: int = 1, **kwargs):
            self._counter.inc(value)


    class GaugeComm(Comm):
        def __init__(self, counter: Counter):
            self._counter = counter

        def send(self, value: int = 1, **kwargs):
            self._counter.set(value)


    def _wrap_metric(metric: Counter|Gauge) -> CounterComm|GaugeComm:
        if isinstance(metric, Counter):
            return CounterComm(metric)
        if isinstance(metric, Gauge):
            return GaugeComm(metric)
        raise ValueError(f"PrometheusComm expects either Counter or Gauge, not {metric.__class__.__name__}")


    class PrometheusComm(Comm):
        def __init__(self, input: dict[Enum,Counter|Gauge], port: int = 8000):
            start_http_server(port)
            self._metrics = {
                kind: _wrap_metric(metric)
                for kind, metric in input.items()
            }

        def send(self, *kinds: Enum, value: int = 1, **kwargs):
            for kind in kinds:
                self._metrics[kind].send(value, **kwargs)
else:
    class Counter:
        def __init__(self, *args, **kwargs):
            raise ImportError(_get_import_error("Counter", "prometheus"))


    class Gauge:
        def __init__(self, *args, **kwargs):
            raise ImportError(_get_import_error("Gauge", "prometheus"))


    class PrometheusComm:
        def __init__(self, *args, **kwargs):
            raise ImportError(_get_import_error("PrometheusComm", "prometheus"))
