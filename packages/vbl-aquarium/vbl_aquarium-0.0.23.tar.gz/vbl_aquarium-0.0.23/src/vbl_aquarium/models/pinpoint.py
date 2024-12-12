from __future__ import annotations

from pydantic import Field

from vbl_aquarium.models.unity import Color, Vector2, Vector3
from vbl_aquarium.utils.vbl_base_model import VBLBaseModel

# CRANIOTOMY


class CraniotomyModel(VBLBaseModel):
    index: int
    size: Vector2
    position: Vector3


# TRANSFORM


class AffineTransformModel(VBLBaseModel):
    name: str
    prefix: str
    scaling: Vector3
    rotation: Vector3


# RIG


class RigModel(VBLBaseModel):
    name: str
    image: str
    position: Vector3 = Field(default=Vector3(x=0, y=0, z=0))
    rotation: Vector3 = Field(default=Vector3(x=0, y=0, z=0))
    active: bool


# Probes and insertions


class InsertionModel(VBLBaseModel):
    position: Vector3
    angles: Vector3
    atlas_name: str
    transform_name: str
    reference_coord: Vector3


class ProbeModel(VBLBaseModel):
    insertion: InsertionModel

    uuid: str
    name: str

    color: Color


# Full scene


class SceneModel(VBLBaseModel):
    atlas_name: str
    transform_name: str

    probes: list[ProbeModel]
    rigs: list[RigModel]
    craniotomies: list[CraniotomyModel]

    scene_data: list[str]

    settings: str
