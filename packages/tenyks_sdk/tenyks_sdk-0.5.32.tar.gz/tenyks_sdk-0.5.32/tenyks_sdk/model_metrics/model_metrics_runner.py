import io
import logging
import traceback
from datetime import datetime, timezone

from tenyks_sdk.file_providers.single_file_provider_factory import (
    SingleFileProviderFactory,
)
from tenyks_sdk.model_metrics.datatypes import ModelMetricInput, ModelMetricOutput
from tenyks_sdk.model_metrics.model_metrics_factory import ModelMetricsFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelMetricsRunner:
    def __init__(
        self,
        model_metric_input: ModelMetricInput,
        model_metrics_registry: str,
    ) -> None:
        self.model_metric_input = model_metric_input
        self.model_metrics_factory = ModelMetricsFactory(model_metrics_registry)

    def run_metric_and_save_output(
        self,
        debug: bool = False,
    ):
        metric_name = self.model_metric_input.metric_name
        model_metric_computer = self.model_metrics_factory.get_model_metric(
            metric_name, self.model_metric_input
        )

        logger.info(f"Starting run for metric: {metric_name}")
        metric_run_started_at = datetime.now(timezone.utc)

        try:
            metric_results = model_metric_computer.run_metric()
            logger.info(
                f"Completed run for metric: {metric_name} started at {metric_run_started_at}."
            )
        except Exception as e:
            logger.error(
                f"FAILED run for metric: {metric_name} with error '{e}'. Details below:"
            )
            logger.error(traceback.format_exc())
            raise e

        metric_output = ModelMetricOutput(
            started_at=metric_run_started_at.isoformat(), results=metric_results
        )
        metric_output_json = metric_output.to_json()

        output_location_provider = (
            SingleFileProviderFactory.create_file_provider_from_location(
                self.model_metric_input.metric_results_file_location
            )
        )
        if debug:
            print(f"== Final Metric Result: {metric_output_json}")

        logger.info("Saving Model Metric results to the output location.")
        output_location_provider.save_content(
            io.BytesIO(metric_output_json.encode("utf-8"))
        )
        logger.info("Done saving Model Metrics results to the output location.")
