from storages.backends.s3boto3 import S3Boto3Storage
from botocore.config import Config
from botocore.vendored.requests.exceptions import ConnectTimeout

from django.conf import settings
from django.utils.translation import gettext as _

from zs_utils.exceptions import CustomException


class S3Boto3StorageException(CustomException):
    status_code = 500


class CustomS3Boto3Storage(S3Boto3Storage):
    location = settings.AWS_MEDIA_ROOT
    default_acl = "public-read"
    config = Config(
        connect_timeout=settings.AWS_CONNECT_TIMEOUT,
        read_timeout=settings.AWS_READ_TIMEOUT,
        retries={
            "max_attempts": settings.AWS_CONNECT_MAX_RETRY_ATTEMPTS,
        },
    )

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except ConnectTimeout:
            raise S3Boto3StorageException(message=_("Проблемы с доступом к файловому хранилищу."))
