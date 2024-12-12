from abc import ABC, abstractmethod
from typing import List

from tenyks_sdk.data_quality_check.datatypes import (
    DqcDependency,
    DQCIndividualCheckResult,
    DQCInput,
    DqcRunsOn,
)


class DataQualityCheck(ABC):
    @classmethod
    @abstractmethod
    def create(cls, dqc_input: DQCInput) -> "DataQualityCheck":
        pass

    @classmethod
    @abstractmethod
    def get_check_type(cls):
        raise NotImplementedError()

    @abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_display_name(cls) -> str:
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def get_dependencies(cls) -> List[DqcDependency]:
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def runs_on(cls) -> DqcRunsOn:
        return NotImplementedError()

    @abstractmethod
    def perform_check(self) -> List[DQCIndividualCheckResult]:
        raise NotImplementedError()
