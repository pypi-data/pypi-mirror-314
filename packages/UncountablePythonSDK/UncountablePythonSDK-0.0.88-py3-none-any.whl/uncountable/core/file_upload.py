import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from io import BytesIO
from pathlib import Path
from typing import Generator, Literal, Self

import aiohttp
import aiotus

from .types import AuthDetailsAll, AuthDetailsApiKey

_CHUNK_SIZE = 5 * 1024 * 1024  # s3 requires 5MiB minimum


class FileUploadType(StrEnum):
    MEDIA_FILE_UPLOAD = "MEDIA_FILE_UPLOAD"
    DATA_FILE_UPLOAD = "DATA_FILE_UPLOAD"


@dataclass(kw_only=True)
class MediaFileUpload:
    """Upload file from a path on disk"""

    path: str
    type: Literal[FileUploadType.MEDIA_FILE_UPLOAD] = FileUploadType.MEDIA_FILE_UPLOAD


@dataclass(kw_only=True)
class DataFileUpload:
    data: BytesIO
    name: str
    type: Literal[FileUploadType.DATA_FILE_UPLOAD] = FileUploadType.DATA_FILE_UPLOAD


FileUpload = MediaFileUpload | DataFileUpload


@dataclass(kw_only=True)
class FileBytes:
    name: str
    bytes_data: BytesIO


@contextmanager
def file_upload_data(file_upload: FileUpload) -> Generator[FileBytes, None, None]:
    match file_upload:
        case MediaFileUpload():
            with open(file_upload.path, "rb") as f:
                yield FileBytes(
                    name=Path(file_upload.path).name, bytes_data=BytesIO(f.read())
                )
        case DataFileUpload():
            yield FileBytes(name=file_upload.name, bytes_data=file_upload.data)


@dataclass(kw_only=True)
class UploadedFile:
    name: str
    file_id: int


class UploadFailed(Exception):
    pass


class FileUploader:
    _auth_details: AuthDetailsAll
    _base_url: str
    _allow_insecure_tls: bool

    def __init__(
        self: Self,
        base_url: str,
        auth_details: AuthDetailsAll,
        allow_insecure_tls: bool = False,
    ) -> None:
        self._base_url = base_url
        self._auth_details = auth_details
        self._allow_insecure_tls = allow_insecure_tls

    async def _upload_file(self: Self, file_upload: FileUpload) -> UploadedFile:
        creation_url = f"{self._base_url}/api/external/file_upload/files"
        if not isinstance(self._auth_details, AuthDetailsApiKey):
            raise NotImplementedError("Unsupported authentication method.")

        auth = aiohttp.BasicAuth(
            self._auth_details.api_id, self._auth_details.api_secret_key
        )
        async with (
            aiohttp.ClientSession(
                auth=auth, headers={"Origin": self._base_url}
            ) as session,
        ):
            with file_upload_data(file_upload) as file_bytes:
                location = await aiotus.upload(
                    creation_url,
                    file_bytes.bytes_data,
                    {"filename": file_bytes.name.encode()},
                    client_session=session,
                    config=aiotus.RetryConfiguration(ssl=not self._allow_insecure_tls),
                    chunksize=_CHUNK_SIZE,
                )
                if location is None:
                    raise UploadFailed(f"Failed to upload: {file_bytes.name}")
                return UploadedFile(
                    name=file_bytes.name, file_id=int(location.path.split("/")[-1])
                )

    def upload_files(
        self: Self, *, file_uploads: list[FileUpload]
    ) -> list[UploadedFile]:
        return [
            asyncio.run(self._upload_file(file_upload)) for file_upload in file_uploads
        ]
