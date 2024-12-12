import importlib

from tenyks_sdk.model_metrics.datatypes import ModelMetricInput
from tenyks_sdk.model_metrics.model_metric import ModelMetric


class ModelMetricsFactory:
    def __init__(
        self,
        model_metrics_registry: str,
    ) -> None:

        try:
            metric_module = importlib.import_module(model_metrics_registry)
            self._model_metrics_registry = getattr(
                metric_module, "model_metrics_registry"
            )
        except ImportError:
            raise FileNotFoundError(f"No registry found at '{model_metrics_registry}'")

    def get_model_metric(
        self, metric_name: str, model_metric_input: ModelMetricInput
    ) -> ModelMetric:
        model_metric = self._model_metrics_registry.get(metric_name)

        if not model_metric:
            raise ValueError(f"Metric '{metric_name}' not found in the registry.")

        return model_metric.create(model_metric_input)
