import dataclasses
from io import BytesIO
from typing import ClassVar, Tuple, Optional, Dict
from urllib.parse import urlparse
import pyarrow.dataset as ds
import boto3
import pandas as pd


@dataclasses.dataclass(frozen=True)
class AWSConfig:
    """
    AWS configuration for the task
    """
    aws_region: Optional[str] = None
    aws_endpoint_url: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    def to_kwargs(self) -> Dict[str, str]:
        """
        Convert the AWSConfig to kwargs for the AWSIoContext
        :return: The kwargs
        """
        return {
            key: value
            for key, value in dataclasses.asdict(self).items()
            if value is not None
        }



@dataclasses.dataclass
class AWSIoContext:
    """
    Context for AWS IO operations, to allow for easy mocking / testing. If no context is set, the default boto3 client
    will be used.
    """
    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    aws_session_token: str = None
    aws_endpoint_url: str = None
    aws_region: str = None
    _current: ClassVar['AWSIoContext'] = None

    @classmethod
    def get_boto3_client(cls) -> boto3.session.Session.client:
        """
        Retrieve a boto3 client. If no context is set, the default boto3 client will be used.
        :return:
        """
        if cls._current is None:
            return boto3.client('s3')
        return cls._current._get_boto3_client()

    def _get_boto3_client(self) -> boto3.session.Session.client:
        """
        Retrieve a boto3 session
        :return:
        """
        kwargs = {}
        if self.aws_access_key_id:
            kwargs['aws_access_key_id'] = self.aws_access_key_id
        if self.aws_secret_access_key:
            kwargs['aws_secret_access_key'] = self.aws_secret_access_key
        if self.aws_session_token:
            kwargs['aws_session_token'] = self.aws_session_token
        if self.aws_endpoint_url:
            kwargs['endpoint_url'] = self.aws_endpoint_url
        if self.aws_region:
            kwargs['region_name'] = self.aws_region

        return boto3.client(
            's3',
            **kwargs
        )

    def __enter__(self):
        AWSIoContext._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        AWSIoContext._current = None


def validate_s3_uri(s3_uri: str) -> bool:
    """
    Validates an S3 URI
    :param s3_uri: The S3 URI to validate. S3 URIs must be of the form s3://bucket/key
    :return: True if the URI is valid, False otherwise
    """
    if not s3_uri.startswith('s3://'):
        return False
    if s3_uri.count('/') < 3:
        return False
    if s3_uri.endswith('/'):
        return False
    return True


def validate_s3_dir_uri(s3_uri: str) -> bool:
    """
    Validates an S3 URI for a directory in S3
    :param s3_uri: The S3 URI to validate. S3 dir URIs must be of the form s3://bucket/key/
    :return: True if the URI is valid, False otherwise
    """
    if not s3_uri.startswith('s3://'):
        return False
    if s3_uri.count('/') < 3:
        return False
    if not s3_uri.endswith('/'):
        return False
    return True


def s3_uri_to_bucket_key(s3_uri: str) -> Tuple[str, str]:
    """
    Convert an S3 URI to a bucket name and key
    :param s3_uri: S3 URI to convert
    :return: A tuple of (bucket_name, key)
    """
    parsed_url = urlparse(s3_uri)
    bucket_name = parsed_url.netloc
    directory_name = parsed_url.path[1:]
    return bucket_name, directory_name


def get_metadata(s3_uri: str) -> dict:
    """
    Get the metadata of an S3 object
    :param s3_uri: S3 URI
    :return: Metadata
    """
    assert validate_s3_uri(s3_uri), f'Invalid S3 URI: {s3_uri}'
    s3_client = AWSIoContext.get_boto3_client()
    bucket, key = s3_uri_to_bucket_key(s3_uri)
    metadata = s3_client.head_object(
        Bucket=bucket,
        Key=key
    )
    return metadata


def s3_listdir(s3_uri, max_list_len=1000):
    """
    Replicates os.listdir() functionality for boto3. Returns a list of all objects underneath the
    folder `directory_name` in Bucket `bucket_name`, including those in subfolders.

    Note that S3 does not have a concept of folders, so this function will return all objects that begin with the
    supplied s3_uri. This means that if you have a folder structure like:
    - s3://bucket/folder1/folder2/file1
    - s3://bucket/folder1/folder2/file2
    - s3://bucket/folder1/folder3/file3
    And you call s3_listdir(s3://bucket/folder1/fold), you will get back:
    - s3://bucket/folder1/folder2/file1
    - s3://bucket/folder1/folder2/file2
    - s3://bucket/folder1/folder3/file3
    Even though there is no folder called "fold".

    :param s3_uri: S3 uri to list
    :param max_list_len: Max items to return in initial list

    :return: list of strings giving the names of all objects in the directory `directory_name`
    """
    assert validate_s3_dir_uri(s3_uri), f'Invalid S3 dir URI: {s3_uri}'
    client = AWSIoContext.get_boto3_client()
    bucket_name, directory_name = s3_uri_to_bucket_key(s3_uri)
    is_truncated = True
    continuation_token = None
    keys = []
    while is_truncated:
        if continuation_token is None:
            response = client.list_objects_v2(Bucket=bucket_name, Prefix=directory_name, MaxKeys=max_list_len)
            if response['KeyCount'] == 0:
                return []
        else:
            response = client.list_objects_v2(Bucket=bucket_name,
                                              Prefix=directory_name,
                                              MaxKeys=max_list_len,
                                              ContinuationToken=continuation_token)
        is_truncated = response.get('IsTruncated', False)
        continuation_token = response.get('NextContinuationToken', None)
        keys += [obj.get('Key') for obj in response['Contents']]

    return [f"s3://{bucket_name}/{key}" for key in keys]


def s3_new_bucket(bucket: str) -> None:
    """
    Create a new S3 bucket
    :param bucket: name of bucket to create
    :return:
    """
    s3_client = AWSIoContext.get_boto3_client()
    s3_client.create_bucket(
        Bucket=bucket
    )


def s3_put(s3_uri: str, data: bytes, content_type: str = None, metadata: dict = None) -> None:
    """
    Put data to S3
    :param s3_uri: S3 URI
    :param data: Data to put
    :param content_type: Content type
    :param metadata: Metadata
    :return:
    """
    validate_s3_uri(s3_uri)
    s3_client = AWSIoContext.get_boto3_client()
    bucket, key = s3_uri_to_bucket_key(s3_uri)
    kwargs = {"Bucket": bucket, "Key": key, "Body": data}
    if content_type:
        kwargs['ContentType'] = content_type
    if metadata:
        kwargs['Metadata'] = metadata

    s3_client.put_object(
        **kwargs
    )


def s3_get(s3_uri: str) -> bytes:
    """
    Get data from S3
    :param s3_uri: S3 URI
    :return: Data
    """
    validate_s3_uri(s3_uri)
    s3_client = AWSIoContext.get_boto3_client()
    bucket, key = s3_uri_to_bucket_key(s3_uri)
    obj = s3_client.get_object(
        Bucket=bucket,
        Key=key
    )
    return obj['Body'].read()


def load_parquet_files_from_s3(s3_uri: str) -> pd.DataFrame:
    """
    Loads a group of parquet files from S3 into a single dataframe utilizing Pandas.
    Note that we cannot use the S3 URI directly with pandas because moto doesn't support it.

    :param s3_uri: S3 URI to the parquet files
    :return: Pandas dataframe
    """
    assert validate_s3_dir_uri(s3_uri), f'Invalid S3 dir URI: {s3_uri}'
    files = list(s3_listdir(s3_uri))
    dfs = []
    for file in files:
        dfs.append(pd.read_parquet(BytesIO(s3_get(file))))
    return pd.concat(dfs, ignore_index=True)


def get_parquet_file_metadata(s3_uri: str) -> Tuple[int, int]:
    """
    Get the metadata of a parquet file. Note that this is not moto compatible.
    :param s3_uri:
    :return: A tuple of (number of columns, number of rows)
    """
    assert validate_s3_uri(s3_uri), f'Invalid S3 URI: {s3_uri}'
    dataset = ds.dataset(s3_uri)
    n_columns = len(dataset.schema.names)
    total_n_rows = 0
    for batch in dataset.to_batches(columns=[dataset.schema.names[0]], batch_size=500000):
        total_n_rows += batch.num_rows
    return n_columns, total_n_rows

