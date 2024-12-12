from tenyks_sdk.data_quality_check.datatypes import DQCOutput


class DQCSerializer:
    @staticmethod
    def serialize_dqc(dqc_output: DQCOutput) -> str:
        json = dqc_output.to_json()
        return json

    @staticmethod
    def deserialize_dqc(json: str) -> DQCOutput:
        dqc_output = DQCOutput.from_json(json)
        return dqc_output
