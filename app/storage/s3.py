from contextlib import asynccontextmanager
from uuid import UUID

import aioboto3
from fastapi import UploadFile

from app.config import s3_config


class S3Storage:
    def __init__(self):
        self.bucket_name = s3_config.S3_BUCKET
        self.session = aioboto3.Session()

    @asynccontextmanager
    async def get_s3_client(self):
        async with self.session.client(
            service_name="s3",
            endpoint_url=s3_config.S3_ENDPOINT,
            aws_access_key_id=s3_config.S3_ACCESS_KEY,
            aws_secret_access_key=s3_config.S3_SECRET_KEY,
            region_name=s3_config.S3_REGION,
        ) as s3_client:
            yield s3_client

    async def upload_file(
        self,
        file: UploadFile,
        uuid_obj: UUID | str,
        root_dir: str = "images",
        is_needed_bucket_name_in_url: bool = False,
    ) -> str:
        async with self.get_s3_client() as s3_client:
            file.file.seek(0)
            object_name = f"{root_dir}/{str(uuid_obj)}/{file.filename}"
            await s3_client.upload_fileobj(file.file, self.bucket_name, object_name)

            if is_needed_bucket_name_in_url:
                return f"{s3_config.S3_PUBLIC_URL}/{self.bucket_name}/{object_name}"
            return f"{s3_config.S3_PUBLIC_URL}/{object_name}"

    async def delete_file(self, url: str) -> None:
        object_name = url.replace(f"{s3_config.S3_PUBLIC_URL}/", "").lstrip("/")
        async with self.get_s3_client() as s3_client:
            await s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
