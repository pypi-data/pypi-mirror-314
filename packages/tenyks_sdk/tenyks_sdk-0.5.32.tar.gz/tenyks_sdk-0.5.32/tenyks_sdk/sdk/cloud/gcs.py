import re
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, SecretStr

from tenyks_sdk.sdk.cloud.dataclasses import CloudLocationType

_gcs_uri_pattern = re.compile(
    r"^gs://"
    r"[a-z0-9\.\-_]+/"  # Bucket name constraints (lowercase, numbers, dots, hyphens, underscores)
    r"([a-zA-Z0-9\-_]+/)*"  # Optional directory path (letters, numbers, hyphens, underscores)
    r"[a-zA-Z0-9\-_]*[a-zA-Z0-9\-_\.]*$"  # File or folder name, allowing for periods
)


class GCSLocation(BaseModel):
    """
    Represents a Google Cloud Storage (GCS) location, including a URI and the necessary service account credentials.

    Attributes:\n
        type (str): \n
            GCS location type. This is frozen and defaults to `CloudLocationType.GCS.value`.
            **Default**: "gcs"

        gcs_uri (str): \n
            GCS URI indicating the location in Google Cloud Storage.\n
            **Examples**: ["gs://bucket-name/path/to/folder_or_file"]\n
            **Constraints**: Must match the GCS URI pattern and will have whitespace stripped.

        credentials (Dict[str, SecretStr]): \n
            GCS service account credentials in JSON format.\n
            **Examples**:
                - {
                    "type": "service_account",
                    "project_id": "my-project-id",
                    "private_key_id": "************",
                    "private_key": "-----BEGIN PRIVATE KEY-----\\n...",
                    "client_email": "my-service-account@example.com",
                    "client_id": "************",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-service-account@example.com",
                  }
    """

    type: str = Field(
        default=CloudLocationType.GCS.value,
        description="GCS Location type",
        frozen=True,
    )
    gcs_uri: str = Field(
        description="GCS URI",
        examples=[
            "gs://bucket-name/path/to/folder_or_file",
        ],
        strip_whitespace=True,
        pattern=_gcs_uri_pattern,
    )
    credentials: Optional[Dict[str, SecretStr]] = Field(
        default=None,
        description="GCS service account credentials in JSON format",
        examples=[
            {
                "type": "service_account",
                "project_id": "my-project-id",
                "private_key_id": "my-private-key-id",
                "private_key": "-----BEGIN PRIVATE KEY-----\n...",
                "client_email": "my-service-account@example.com",
                "client_id": "my-client-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-service-account@example.com",
            }
        ],
    )

    def model_dump(self, **kwargs) -> Dict[str, Union[str, Dict[str, Any]]]:
        gcs_location_dict = super().model_dump(**kwargs)
        gcs_location_dict["credentials"] = {
            key: value.get_secret_value() for key, value in self.credentials.items()
        }
        return gcs_location_dict
