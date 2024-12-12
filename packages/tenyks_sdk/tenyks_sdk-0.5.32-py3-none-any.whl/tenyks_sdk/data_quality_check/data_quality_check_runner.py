import io
import logging
import traceback
from datetime import datetime, timezone
from typing import List

from tenyks_sdk.data_quality_check.data_quality_check import DataQualityCheck
from tenyks_sdk.data_quality_check.data_quality_check_factory import DQCFactory
from tenyks_sdk.data_quality_check.datatypes import DQCInput
from tenyks_sdk.data_quality_check.result_assembler import DQCResultAssembler
from tenyks_sdk.data_quality_check.serialization import DQCSerializer
from tenyks_sdk.file_providers.single_file_provider_factory import (
    SingleFileProviderFactory,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DQCRunner:

    def __init__(self, dqc_input: DQCInput, data_quality_checks_registy: str) -> None:
        self.dqc_input = dqc_input
        self.dqc_registry = data_quality_checks_registy
        self.checks_to_run = set(self.dqc_input.check_types)

    def run_checks_and_save_output(self):
        dqc_factory = DQCFactory(self.dqc_registry)
        checks: List[DataQualityCheck] = [
            dqc_factory.get_dqc_check(check_type, self.dqc_input)
            for check_type in self.checks_to_run
        ]

        logger.info(f"DQC checks to be performed: {self.checks_to_run}")
        output_assembler = DQCResultAssembler()
        for check in checks:
            check_type = check.get_check_type()
            check_display_name = check.get_display_name()
            logger.info(f"Starting check for DQC '{check_type}'")

            check_started_at = datetime.now(timezone.utc)
            try:
                check_results = check.perform_check()
                logger.info(f"Completed check for DQC '{check_type}'")
                output_assembler.append_completed_check(
                    check_type,
                    check_display_name,
                    check_results,
                    check_started_at,
                    check.get_version(),
                    check.get_description(),
                )
            except Exception as e:
                logger.error(
                    f"FAILED check for DQC '{check_type}' with error '{e}'. "
                    "Details below:"
                )
                logger.error(traceback.format_exc())
                output_assembler.append_failed_check(
                    check_type,
                    check_display_name,
                    str(e),
                    check_started_at,
                    check.get_version(),
                    check.get_description(),
                )
        logger.info("Done performing all checks.")

        assembled_output = output_assembler.assemble()
        assembled_output_json = DQCSerializer.serialize_dqc(assembled_output)

        output_location_provider = (
            SingleFileProviderFactory.create_file_provider_from_location(
                self.dqc_input.output_location
            )
        )

        logger.info("Saving DQC results to the output location.")
        output_location_provider.save_content(
            io.BytesIO(assembled_output_json.encode("utf-8"))
        )
        logger.info("Done saving DQC results to the output location.")
