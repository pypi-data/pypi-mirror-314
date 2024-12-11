import datetime
from typing import Annotated, Any, Literal, TypeAlias
import pydantic


def _hex_bytes_validator(val: Any) -> bytes:
    if isinstance(val, bytes):
        return val
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, str):
        return bytes.fromhex(val)
    raise ValueError(f"Invalid hex bytes: {val}")


HexBytes: TypeAlias = Annotated[
    bytes,
    pydantic.PlainValidator(_hex_bytes_validator),
    pydantic.PlainSerializer(lambda v: v.hex()),
]


class IntranetUrlSpec(pydantic.BaseModel):
    spec_kind: Literal["intranet_url"] = "intranet_url"
    retrieved_at: datetime.datetime
    original_url: str
    actual_url: str
    headers: dict[str, str]
    blob_hash: HexBytes


class PublicUrlSpec(pydantic.BaseModel):
    spec_kind: Literal["public_url"] = "public_url"
    url: str


class FileUploadSpec(pydantic.BaseModel):
    spec_kind: Literal["file_upload"] = "file_upload"
    uploaded_at: datetime.datetime
    original_filename: str
    blob_hash: HexBytes


class ScraperSpec(pydantic.BaseModel):
    spec_kind: Literal["scraper"] = "scraper"
    scraper_id: str
    scraper_args: dict[str, object]


IngestionEntrySpec: TypeAlias = (
    IntranetUrlSpec | PublicUrlSpec | FileUploadSpec | ScraperSpec
)


class IngestionJobSpec(pydantic.BaseModel):
    kb_friendly_name: str
    entries: list[IngestionEntrySpec]
