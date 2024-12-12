from __future__ import annotations

from pydantic import Field

from vbl_aquarium.models.unity import Color, Vector2, Vector3
from vbl_aquarium.utils.vbl_base_model import VBLBaseModel


# Standard types and lists
class IDData(VBLBaseModel):
    id: str = Field(..., alias="ID")


class Vector2Data(VBLBaseModel):
    id: str = Field(alias="ID")
    value: Vector2


class Vector3Data(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: Vector3


class Vector3List(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[Vector3]


class ColorData(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: Color


class ColorList(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[Color]


class StringData(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: str


class StringList(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[str]


class FloatData(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: float


class FloatList(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[float]


class IntData(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: int


class IntList(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[int]


class BoolData(VBLBaseModel):
    id: str = Field(..., alias="ID")
    value: bool


class BoolList(VBLBaseModel):
    id: str = Field(..., alias="ID")
    values: list[bool]


# ID lists


class IDList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")


class IDListVector2Data(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: Vector2


class IDListVector2List(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[Vector2]


class IDListVector3Data(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: Vector3


class IDListVector3List(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[Vector3]


class IDListColorData(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: Color


class IDListColorList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[Color]


class IDListStringData(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: str


class IDListStringList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[str]


class IDListFloatData(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: float


class IDListFloatList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[float]


class IDListIntData(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: int


class IDListIntList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[int]


class IDListBoolData(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    value: bool


class IDListBoolList(VBLBaseModel):
    ids: list[str] = Field(..., alias="IDs")
    values: list[bool]
