from abc import ABC, abstractmethod

from tenyks_sdk.model_metrics.datatypes import (
    MetricAggregation,
    MetricType,
    MetricUnifiedInput,
    MetricUnifiedOutput,
)


class UnifiedMetric(ABC):

    @abstractmethod
    def get_metric_type(self) -> MetricType:
        raise NotImplementedError()

    @abstractmethod
    def get_metric_aggregation(self) -> MetricAggregation:
        raise NotImplementedError()

    @abstractmethod
    def run_metric(self, metric_input: MetricUnifiedInput) -> MetricUnifiedOutput:
        raise NotImplementedError()
