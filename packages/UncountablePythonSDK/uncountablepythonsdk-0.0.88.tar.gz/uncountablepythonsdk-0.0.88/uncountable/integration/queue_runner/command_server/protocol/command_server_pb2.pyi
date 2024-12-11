# ruff: noqa
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EnqueueJobRequest(_message.Message):
    __slots__ = ("job_ref_name", "serialized_payload")
    JOB_REF_NAME_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    job_ref_name: str
    serialized_payload: str
    def __init__(
        self,
        job_ref_name: _Optional[str] = ...,
        serialized_payload: _Optional[str] = ...,
    ) -> None: ...

class EnqueueJobResult(_message.Message):
    __slots__ = ("successfully_queued", "queued_job_uuid")
    SUCCESSFULLY_QUEUED_FIELD_NUMBER: _ClassVar[int]
    QUEUED_JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    successfully_queued: bool
    queued_job_uuid: str
    def __init__(
        self, successfully_queued: bool = ..., queued_job_uuid: _Optional[str] = ...
    ) -> None: ...

class CheckHealthRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CheckHealthResult(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
