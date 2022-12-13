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