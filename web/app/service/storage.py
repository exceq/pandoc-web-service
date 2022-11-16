import os

from minio import Minio

# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio(  # todo to env
    "storage:9000",
    access_key="minio",
    secret_key="minio124",
    secure=False
)