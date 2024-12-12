import functools
import json
from typing import Dict

import pandas as pd
from moto import mock_s3

from curia.utils.s3 import s3_uri_to_bucket_key, AWSIoContext


def _create_seed_s3_data(seed_s3_data: Dict[str, dict]):
    if not isinstance(seed_s3_data, dict):
        raise TypeError("seed_s3_data should be a dict!")
    s3_client = AWSIoContext.get_boto3_client()
    created_buckets = set()
    for s3_uri, object_data in seed_s3_data.items():
        bucket, key = s3_uri_to_bucket_key(s3_uri)
        if bucket not in created_buckets:
            s3_client.create_bucket(
                Bucket=bucket
            )
            created_buckets.add(bucket)

        if 'Body' in object_data:
            # sanitize the body intelligently
            if isinstance(object_data['Body'], str):
                object_data['Body'] = object_data['Body'].encode()
            elif isinstance(object_data['Body'], (dict, list)):
                object_data['Body'] = json.dumps(object_data['Body']).encode()
            elif isinstance(object_data['Body'], pd.DataFrame):
                object_data['Body'] = object_data['Body'].to_parquet()

        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            **object_data
        )


def curia_mock_s3(seed_s3_data: Dict[str, dict]):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            _create_seed_s3_data(seed_s3_data)
            return fn(*args, **kwargs)
        wrapper = mock_s3(wrapper)
        return wrapper
    return decorator