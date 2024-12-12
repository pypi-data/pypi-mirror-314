from __future__ import annotations

from vbl_aquarium.utils.vbl_base_model import VBLBaseModel

# File IO


# Models for sending data to dock server
class DockModel(VBLBaseModel):
    dock_url: str


class BucketRequest(VBLBaseModel):
    token: str
    password: str


class UploadRequest(VBLBaseModel):
    type: int
    data: str
    password: str


class DownloadRequest(VBLBaseModel):
    password: str


class DownloadResponse(VBLBaseModel):
    type: str
    data: str


# Models for sending save/load messages
class SaveRequest(VBLBaseModel):
    filename: str = ""
    bucket: str = ""
    password: str = ""


class LoadRequest(VBLBaseModel):
    filename: str = ""
    bucket: str = ""
    password: str = ""


class LoadModel(VBLBaseModel):
    types: list[int]
    data: list[str]
