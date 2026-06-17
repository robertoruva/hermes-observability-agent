from hermes.infrastructure.metrics.fake_metrics_reader import FakeMetricsReader
from hermes.ports.metrics_reader import MetricsReader


def create_metrics_reader() -> MetricsReader:
    return FakeMetricsReader()
