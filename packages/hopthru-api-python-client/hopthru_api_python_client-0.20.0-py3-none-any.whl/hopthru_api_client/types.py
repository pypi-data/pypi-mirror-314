from datetime import date
from enum import Enum
from typing_extensions import TypedDict
from uuid import UUID


class APCExtractionInterval(Enum):
    WEEKLY = 1
    MONTHLY = 2


class ApiKeyAuth(TypedDict):
    api_key: str


class AgencyReportsConfig(TypedDict):
    use_expanded_data: bool
    show_atypical_days: bool


class UserNamePasswordAuth(TypedDict):
    username: str
    password: str


class UploadDateDict(TypedDict):
    start_date: date
    end_date: date


class FileUploadFormFields(TypedDict):
    key: str
    AWSAccessKeyId: str
    policy: str
    signature: str


class DateRangeFileUploadDict(TypedDict):
    id: UUID
    uploadUrlExpiry: int
    uploadUrl: str
    uploadFormFields: FileUploadFormFields


class DateRangeFileUploadGroup(TypedDict):
    id: UUID
    groupType: str
    groupStatus: str
    startDate: date
    endDate: date
    hasManyItems: bool
    metadata: dict
