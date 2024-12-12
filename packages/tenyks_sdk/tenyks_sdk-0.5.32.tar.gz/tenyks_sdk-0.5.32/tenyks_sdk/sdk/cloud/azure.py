import re
from enum import Enum
from typing import Any, Dict, Optional, Union
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, Field, SecretStr, model_validator

from tenyks_sdk.sdk.cloud.dataclasses import CloudLocationType

_azure_uri_pattern = re.compile(
    r"^https://"
    r"[a-z0-9-]+\."  # Account name (lowercase, numbers, hyphens)
    r"(blob|file|queue|table)"  # Service type
    r"\.core\.windows\.net/"  # Azure core domain
    r"([a-zA-Z0-9_-]+/)*"  # Container/share/queue/table and directories (optional)
    r"[a-zA-Z0-9._-]*$"  # Blob/file/table/queue name, allowing for periods
)


class AzureTokenType(str, Enum):
    CONNECTION_STRING = "connection_string"
    SAS_TOKEN = "sas"


class AzureCredentials(BaseModel):
    """
    Represents Azure credentials required for accessing Azure services.\n

    Attributes:\n
            type (AzureTokenType): \n
                    Azure token type, indicating the type of authentication used.\n
                    **Examples**: [AzureTokenType.CONNECTION_STRING, AzureTokenType.SAS_TOKEN]\n

            value (SecretStr): \n
                    Azure token value, which could be a connection string or a SAS token.\n
                    **Examples**:
                            - "DefaultEndpointsProtocol=https;AccountName=your_account_name;AccountKey=*************;"
                                "EndpointSuffix=core.windows.net"\n
                            - "sv=2020-08-04&ss=b&srt=sco&sp=rwdlacx&se=2022-12-31T23:59:59Z&st=2022-01-01T00:00:00Z&"
                                "spr=https&sig=abcd************ijkl9012mnop3456qrst7890uvwx1234yzab************"
    """

    type: AzureTokenType = Field(
        description="Azure token type",
        examples=[AzureTokenType.CONNECTION_STRING, AzureTokenType.SAS_TOKEN],
    )
    value: SecretStr = Field(
        description="Azure token value",
        examples=[
            "DefaultEndpointsProtocol=https;AccountName=your_account_name;"
            "AccountKey=your_account_key;EndpointSuffix=core.windows.net",
            "sv=2020-08-04&ss=b&srt=sco&sp=rwdlacx&se=2022-12-31T23:59:59Z&st=2022-01-01T00:00:00Z&"
            "spr=https&sig=abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234yzab5678cdef9012",
        ],
    )

    @model_validator(mode="before")
    @classmethod
    def validate_token(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["type"] == AzureTokenType.CONNECTION_STRING:
            if not cls._is_connection_string_valid(values["value"]):
                raise ValueError(
                    "Invalid Azure connection string format. Use the following format: "
                    "DefaultEndpointsProtocol=https;"
                    "AccountName=your_account_name;"
                    "AccountKey=your_account_key;EndpointSuffix=core.windows.net"
                )
        elif values["type"] == AzureTokenType.SAS_TOKEN:
            if not cls._is_sas_url_valid(values["value"]):
                raise ValueError(
                    "Invalid Azure container SAS URL. Use the following format: "
                    "https://<storage_account>.<service>.core.windows.net/<resource_path>?<sas_token>"
                )
        else:
            raise ValueError(f"Unknown Azure token type {values['type']}.")
        return values

    @staticmethod
    def _is_sas_url_valid(sas_value: str) -> bool:
        try:
            parsed_url = urlparse(sas_value)
            parameters = parse_qs(parsed_url.query)

            if parsed_url.scheme.lower() != "https":
                return False

            # Required SAS token fields
            required_fields = ["sv", "sp", "se", "sig"]

            if all(field in parameters for field in required_fields):
                return True
            else:
                return False
        except Exception:
            return False

    def _is_connection_string_valid(connection_string_value: str) -> bool:
        required_parts = ["AccountName", "AccountKey"]
        return all(part in connection_string_value for part in required_parts)

    def model_dump(self, **kwargs) -> Dict[str, Union[str, dict]]:
        azure_credentials_dict = super().model_dump(**kwargs)
        azure_credentials_dict["value"] = self.value.get_secret_value()
        return azure_credentials_dict


class AzureLocation(BaseModel):
    """
    Represents an Azure location, including a URI and the necessary Azure credentials.

    Attributes:
        type (str):
            Azure location type. This is frozen and defaults to `CloudLocationType.AZURE.value`.
            **Default**: "azure"

        azure_uri (str):
            Azure URI indicating the location in Azure services (e.g., Blob, File, Queue, or Table storage). \n
            **Examples**: \n
                - "https://account_name.blob.core.windows.net/container_name/blob_name"\n
                - "https://account_name.file.core.windows.net/share_name/directory_name/file_name"\n
                - "https://account_name.queue.core.windows.net/queue_name"\n
                - "https://account_name.table.core.windows.net/table_name" \n
            **Constraints**: Must match the Azure URI pattern and will have whitespace stripped.

        credentials (AzureCredentials):
            Azure credentials required to access the specified Azure URI. \n
            **Examples**: \n
                - AzureCredentials(
                    type=AzureTokenType.CONNECTION_STRING,
                    value=(
                        "DefaultEndpointsProtocol=https;AccountName=your_account_name;"
                        "AccountKey=*************;EndpointSuffix=core.windows.net"
                    ),
                  )
    """

    type: str = Field(
        default=CloudLocationType.AZURE.value,
        description="Azure Location type",
        frozen=True,
    )
    azure_uri: str = Field(
        description="Azure URI",
        examples=[
            "https://account_name.blob.core.windows.net/container_name/blob_name",
            "https://account_name.file.core.windows.net/share_name/directory_name/file_name",
            "https://account_name.queue.core.windows.net/queue_name",
            "https://account_name.table.core.windows.net/table_name",
        ],
        strip_whitespace=True,
        pattern=_azure_uri_pattern,
    )
    credentials: Optional[AzureCredentials] = Field(
        default=None,
        description="Azure credentials",
        examples=[
            AzureCredentials(
                type=AzureTokenType.CONNECTION_STRING,
                value=(
                    "DefaultEndpointsProtocol=https;AccountName=your_account_name;"
                    "AccountKey=your_account_key;EndpointSuffix=core.windows.net"
                ),
            ),
        ],
    )

    def model_dump(self, **kwargs) -> Dict[str, Union[str, dict]]:
        azure_location_dict = super().model_dump(**kwargs)
        azure_location_dict["credentials"] = self.credentials.model_dump()
        return azure_location_dict
