from abc import ABC, abstractmethod
from typing import Dict, List

from tenyks_sdk.model_metrics.datatypes import ModelMetricInput


class ModelMetric(ABC):

    @classmethod
    @abstractmethod
    def create(
        cls,
        model_metric_input: ModelMetricInput,
    ) -> "ModelMetric":
        pass

    @classmethod
    @abstractmethod
    def get_metric_name(cls):
        raise NotImplementedError()

    @abstractmethod
    def run_metric(self) -> List[Dict]:
        raise NotImplementedError()
