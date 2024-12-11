import json
from functools import cache

import fsspec.utils
import fsspec.utils
from airflow.configuration import conf
from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.json import XComEncoder
from airflow.utils.session import provide_session

SECTION = "common.io"


def _get_compression_suffix(compression: str) -> str:
    """
    Return the compression suffix for the given compression.

    :raises ValueError: if the compression is not supported
    """
    for suffix, c in fsspec.utils.compressions.items():
        if c == compression:
            return suffix

    raise ValueError(f"Compression {compression} is not supported. Make sure it is installed.")


@cache
def _get_compression() -> str | None:
    return conf.get(SECTION, "xcom_objectstorage_compression", fallback=None) or None


@cache
def _get_threshold() -> int:
    return conf.getint(SECTION, "xcom_objectstorage_threshold", fallback=-1)


@cache
def _get_s3_bucket() -> str:
    return conf.get(SECTION, "xcom_objectstorage_bucket", fallback="xcom")


@cache
def _get_conn_name() -> str:
    return conf.get(SECTION, "xcom_objectstorage_conn_id", fallback=None)


class XComObjectStorageBackend(BaseXCom):
    """XCom backend that stores data in S3 if the value exceeds a size threshold."""

    @staticmethod
    def _get_s3_hook() -> S3Hook:
        """Returns an instance of the S3Hook."""
        return S3Hook(aws_conn_id=_get_conn_name())

    @staticmethod
    def _generate_s3_key(task_id: str, dag_id: str, run_id: str, key: str, suff: str) -> str:
        """Generates a unique S3 key for storing the data."""
        return f"xcom/{dag_id}/{run_id}/{task_id}/{key}.json{suff}"

    @staticmethod
    def serialize_value(
            value,
            *,
            key: str = 'return_value',
            task_id: str | None = None,
            dag_id: str | None = None,
            run_id: str | None = None,
            map_index: int | None = None,
    ) -> bytes | str:
        s_val = json.dumps(value, cls=XComEncoder).encode("utf-8")

        if compression := _get_compression():
            suffix = f".{_get_compression_suffix(compression)}"
        else:
            suffix = ""

        threshold = _get_threshold()
        if threshold < 0 or len(s_val) < threshold:  # Either no threshold or value is small enough.
            return s_val

        s3_hook = XComObjectStorageBackend._get_s3_hook()
        bucket_name = _get_s3_bucket()
        s3_key = XComObjectStorageBackend._generate_s3_key(
            task_id,
            dag_id,
            run_id,
            key,
            suffix,
        )

        s3_hook.load_bytes(
            s_val,
            key=s3_key,
            bucket_name=bucket_name,
            replace=True,
        )
        return BaseXCom.serialize_value(s3_key)

    @staticmethod
    def deserialize_value(result) -> any:
        data = BaseXCom.deserialize_value(result)

        if result.value.startswith(b'"xcom/'):
            s3_hook = XComObjectStorageBackend._get_s3_hook()
            bucket_name = _get_s3_bucket()
            s3_key = data

            obj = s3_hook.get_key(s3_key, bucket_name=bucket_name)
            return json.loads(obj.get()["Body"].read())

        return data

    @classmethod
    @provide_session
    def purge(cls, xcom, session) -> None:
        if not isinstance(xcom.value, str):
            return

        if xcom.value.startswith('"xcom/'):
            s3_hook = cls._get_s3_hook()
            bucket_name = cls._get_s3_bucket()
            s3_hook.delete_objects(bucket_name=bucket_name, keys=[xcom.value])

        super().purge(xcom, session)
