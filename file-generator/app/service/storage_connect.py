import os
from os import getenv

from minio import Minio

# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio(
    endpoint=f"{getenv('STORAGE_HOSTNAME')}:9000",
    access_key=getenv("MINIO_ACCESS_KEY"),
    secret_key=getenv("MINIO_SECRET_KEY"),
    secure=False
)


def put_file(bucket_name: str, object_name: str, file_path: str):
    """
    Uploads data from a file to an object in a bucket.

    :param bucket_name: Name of the bucket.
    :param object_name: Object name in the bucket.
    :param file_path: Name of file to upload.
    :return: :class:`ObjectWriteResult` object.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError()

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    return client.fput_object(bucket_name, object_name, file_path)


def put_object(bucket_name: str, object_name: str, data):
    """
    Uploads data from a file to an object in a bucket.

    :param bucket_name: Name of the bucket.
    :param object_name: Object name in the bucket.
    :param data: Data to uplaod.
    :return: :class:`ObjectWriteResult` object.
    """
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    return client.put_object(bucket_name, object_name, data, len(data.data))
