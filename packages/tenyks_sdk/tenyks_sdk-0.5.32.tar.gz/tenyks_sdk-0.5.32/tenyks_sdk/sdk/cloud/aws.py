import re
from typing import Dict, Optional, Union

from pydantic import BaseModel, Field, SecretStr

from tenyks_sdk.sdk.cloud.dataclasses import CloudLocationType

# https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
_s3_uri_pattern = re.compile(
    r"^s3://"  # Bucket name must start with a letter or digit
    r"(?!xn--|sthree-|sthree-configurator|.*-s3alias$)"  # Bucket not start with xn--, sthree-, sthree-configurator or end with -s3alias
    r"(?!.*\.\.)"  # Bucket name must not contain two adjacent periods
    r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]"  # Bucket naming constraints
    r"(?<!\.-)"  # Bucket name must not end with a period followed by a hyphen
    r"(?<!\.)"  # Bucket name must not end with a period
    r"(?<!-)"  # Bucket name must not end with a hyphen
    r"(/([a-zA-Z0-9._-]+/?)*)?$"  # key naming constraints
)


class AWSCredentials(BaseModel):
    """
    Represents AWS credentials required for accessing AWS services.\n

    Attributes:\n
        aws_access_key_id (SecretStr):
            AWS access key ID.\n
            **Examples**: ["AKIA*************AMPLE"]\n

        aws_secret_access_key (SecretStr):
            AWS secret access key.\n
            **Examples**: ["wJalrXUtnFEMI/************EXAMPLEKEY"]\n

        region_name (str):
            AWS region name.\n
            **Examples**: ["eu-central-1"]
    """

    aws_access_key_id: SecretStr = Field(
        description="AWS access key ID", examples=["AKIAIOSFODNN7EXAMPLE"]
    )
    aws_secret_access_key: SecretStr = Field(
        description="AWS secret access key",
        examples=["wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"],
    )
    region_name: str = Field(description="AWS region name", examples=["eu-central-1"])

    def model_dump(self, **kwargs) -> Dict[str, Union[str, dict]]:
        aws_credentials_dict = super().model_dump(**kwargs)
        aws_credentials_dict["aws_access_key_id"] = (
            self.aws_access_key_id.get_secret_value()
        )
        aws_credentials_dict["aws_secret_access_key"] = (
            self.aws_secret_access_key.get_secret_value()
        )
        return aws_credentials_dict


class AWSLocation(BaseModel):
    """
    Represents an AWS location, specifically an S3 URI, along with the necessary AWS credentials.\n

    Attributes:
        type (str): \n
            AWS location type. This is frozen and defaults to `CloudLocationType.AWS_S3.value`.
            **Default**: "aws_s3"\n

        s3_uri (str): \n
            S3 URI indicating the location in the AWS S3 service.
            **Examples**: ["s3://bucket-name/path/to/folder_or_file"]
            **Constraints**: Must match the S3 URI pattern and will have whitespace stripped.

        credentials (AWSCredentials): \n
            AWS credentials required to access the specified S3 URI.\n
            **Examples**:
                - AWSCredentials(
                    aws_access_key_id="AKIA*************AMPLE",
                    aws_secret_access_key="wJalrXUtnFEMI/************EXAMPLEKEY",
                    region_name="eu-central-1",
                  )
    """

    type: str = Field(
        default=CloudLocationType.AWS_S3.value,
        description="Aws Location type",
        frozen=True,
    )
    s3_uri: str = Field(
        description="S3 URI",
        examples=["s3://bucket-name/path/to/folder_or_file"],
        strip_whitespace=True,
        pattern=_s3_uri_pattern,
    )
    credentials: Optional[AWSCredentials] = Field(
        default=None,
        description="AWS credentials",
        examples=[
            AWSCredentials(
                aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
                aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                region_name="eu-central-1",
            )
        ],
    )

    def model_dump(self, **kwargs) -> Dict[str, Union[str, dict]]:
        aws_location_dict = super().model_dump(**kwargs)
        aws_location_dict["credentials"] = self.credentials.model_dump()
        return aws_location_dict
