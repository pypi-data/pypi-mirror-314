import importlib
import logging
from typing import Dict, Type

from tenyks_sdk.data_quality_check.data_quality_check import DataQualityCheck
from tenyks_sdk.data_quality_check.datatypes import DQCInput

logger = logging.getLogger(__name__)


class DQCFactory:
    def __init__(self, data_quality_checks_registy: str) -> None:
        self._dqcs_registry: Dict[str, Type[DataQualityCheck]] = {}
        self._load_custom_dqcs(data_quality_checks_registy)

    def _load_custom_dqcs(self, data_quality_checks_registy: str) -> None:
        try:
            dqc_registry_module = importlib.import_module(data_quality_checks_registy)
            for dqc_type, dqc_class in dqc_registry_module.dqc_registry.items():
                self._register_dqc(dqc_type, dqc_class)
        except ImportError as e:
            logger.error(f"Failed to import DQC from the registry with message: '{e}'")
            raise

    def _register_dqc(self, dqc_type: str, dqc_class: Type[DataQualityCheck]) -> None:
        if dqc_type in self._dqcs_registry:
            logger.warning(
                f"DQC with type '{dqc_type}' is already registered and will be "
                "overwritten."
            )
        self._dqcs_registry[dqc_type] = dqc_class

    def get_dqc_check(self, dqc_type: str, dqc_input: DQCInput) -> DataQualityCheck:
        if dqc_type not in self._dqcs_registry:
            raise KeyError(f"DQC with type '{dqc_type}' is not registered.")
        dqc_class = self._dqcs_registry[dqc_type]
        return dqc_class.create(dqc_input)
