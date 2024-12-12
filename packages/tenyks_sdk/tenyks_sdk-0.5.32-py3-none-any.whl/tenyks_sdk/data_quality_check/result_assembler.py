import logging
from datetime import datetime, timezone
from enum import Enum
from typing import List, Union

from tenyks_sdk.data_quality_check.datatypes import (
    DQCCheckResult,
    DQCCheckStatus,
    DQCIndividualCheckResult,
    DQCOutput,
)

logger = logging.getLogger(__name__)


class DQCResultAssembler:
    def __init__(
        self, job_id: str = "", started_at: datetime = datetime.now(timezone.utc)
    ) -> None:
        self.job_id = job_id
        self.started_at: datetime = started_at
        self.checks: List[DQCCheckResult] = []

    def append_completed_check(
        self,
        check_type: Union[Enum, str],
        display_name: str,
        results: List[DQCIndividualCheckResult],
        started_at: datetime,
        version: str,
        description: str,
        completed_at: datetime = datetime.now(timezone.utc),
    ):
        completed_check = DQCCheckResult(
            check_type,
            display_name,
            version,
            description,
            results,
            started_at.isoformat(),
            completed_at.isoformat(),
            DQCCheckStatus.SUCCESS,
        )
        self.checks.append(completed_check)

    def append_failed_check(
        self,
        check_type: Union[Enum, str],
        display_name: str,
        error_message: str,
        started_at: datetime,
        version: str,
        description: str,
        failed_at: datetime = datetime.now(timezone.utc),
    ):
        failed_check = DQCCheckResult(
            check_type,
            display_name,
            version,
            description,
            [],
            started_at.isoformat(),
            failed_at.isoformat(),
            DQCCheckStatus.FAILED,
            [error_message],
        )
        self.checks.append(failed_check)

    def assemble(
        self, output_assembled_at: datetime = datetime.now(timezone.utc)
    ) -> DQCOutput:
        logger.info("Assembling output of performed checks.")
        output = DQCOutput(
            self.job_id,
            self.started_at.isoformat(),
            output_assembled_at.isoformat(),
            self.checks,
        )

        return output
