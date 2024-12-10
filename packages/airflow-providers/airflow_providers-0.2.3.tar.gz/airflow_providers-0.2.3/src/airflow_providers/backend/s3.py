import json
import uuid

from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.session import provide_session


class XComObjectStorageBackend(BaseXCom):
    """XCom backend that stores data in S3 if the value exceeds a size threshold."""

    @staticmethod
    def _get_s3_hook() -> S3Hook:
        """Returns an instance of the S3Hook."""
        return S3Hook(aws_conn_id="minio")

    @staticmethod
    def _get_s3_bucket() -> str:
        """Returns the S3 bucket name."""
        return "xcom"

    @staticmethod
    def _generate_s3_key(task_id: str, dag_id: str, run_id: str) -> str:
        """Generates a unique S3 key for storing the data."""
        return f"xcom/{dag_id}/{run_id}/{task_id}/{uuid.uuid4()}.json"

    @staticmethod
    def serialize_value(
            value,
            *,
            key: str | None = None,
            task_id: str | None = None,
            dag_id: str | None = None,
            run_id: str | None = None,
            map_index: int | None = None,
    ) -> str:
        """Serializes the value and uploads it to S3 if it exceeds the threshold."""
        serialized_value = json.dumps(value).encode("utf-8")
        threshold = 1024 * 1024  # 1 MB threshold, modify as needed

        if len(serialized_value) < threshold:
            return serialized_value.decode("utf-8")  # Store directly in DB

        # Store in S3
        s3_hook = XComObjectStorageBackend._get_s3_hook()
        bucket_name = XComObjectStorageBackend._get_s3_bucket()
        s3_key = XComObjectStorageBackend._generate_s3_key(task_id, dag_id, run_id)

        s3_hook.load_bytes(
            serialized_value,
            key=s3_key,
            bucket_name=bucket_name,
            replace=True,
        )
        return s3_key

    @staticmethod
    def deserialize_value(result) -> any:
        """Deserializes the value from the database or S3."""
        if result.value.startswith("xcom/"):  # S3 key format
            s3_hook = XComObjectStorageBackend._get_s3_hook()
            bucket_name = XComObjectStorageBackend._get_s3_bucket()
            s3_key = result.value

            obj = s3_hook.get_key(s3_key, bucket_name=bucket_name)
            return json.loads(obj.get()["Body"].read())

        # Value stored in the database
        return json.loads(result.value)

    @staticmethod
    @provide_session
    def purge(xcom, session) -> None:
        """Removes data from S3 if it exists."""
        if xcom.value.startswith("xcom/"):  # S3 key format
            s3_hook = XComObjectStorageBackend._get_s3_hook()
            bucket_name = XComObjectStorageBackend._get_s3_bucket()
            s3_key = xcom.value
            s3_hook.delete_objects(bucket_name=bucket_name, keys=[s3_key])
