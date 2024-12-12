from enum import Enum


class CloudLocationType(str, Enum):
    AWS_S3 = "aws_s3"
    GCS = "gcs"
    AZURE = "azure"
