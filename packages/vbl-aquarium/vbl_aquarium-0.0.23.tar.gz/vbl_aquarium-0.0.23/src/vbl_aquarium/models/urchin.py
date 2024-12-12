from __future__ import annotations

from enum import IntEnum

from pydantic import Field

from vbl_aquarium.models.unity import Color, Vector2, Vector3
from vbl_aquarium.utils.vbl_base_model import VBLBaseModel

# CustomAtlas


class CustomAtlasModel(VBLBaseModel):
    name: str
    dimensions: Vector3
    resolution: Vector3


# Area


class AtlasModel(VBLBaseModel):
    name: str
    reference_coord: Vector3 = None
    areas: list[StructureModel]
    colormap: ColormapModel


class StructureModel(VBLBaseModel):
    name: str
    acronym: str
    atlas_id: int
    color: Color
    # values that come with defaults:
    visible: bool = False
    color_intensity: float = -1
    side: int = 0
    material: str = "default"


# Camera


class CameraModel(VBLBaseModel):
    class CameraMode(IntEnum):
        orthographic = 0
        perspective = 1

    id: str = Field(alias="ID")
    position: Vector3 = None
    rotation: Vector3 = Vector3()
    target: Vector3 = None
    zoom: float = 16
    pan: Vector2 = Vector2()
    mode: CameraMode = Field(
        default=CameraMode.orthographic, json_schema_extra={"enum_keys": list(CameraMode.__members__.keys())}
    )
    background_color: Color = Color()  # white by default
    controllable: bool = True
    main: bool = False


class CameraRotationModel(VBLBaseModel):
    start_rotation: Vector3
    end_rotation: Vector3


# Individual mesh neuron


class PrimitiveMeshModel(VBLBaseModel):
    data: list[MeshModel]


class MeshModel(VBLBaseModel):
    id: str = Field(alias="ID")
    shape: str
    position: Vector3
    color: Color
    scale: Vector3
    material: str
    interactive: bool


# Lines


class LineModel(VBLBaseModel):
    id: str = Field(alias="ID")
    positions: list[Vector3] = Field(default_factory=list)
    color: Color = Color()


# Probes


class ProbeModel(VBLBaseModel):
    id: str = Field(alias="ID")
    position: Vector3
    color: Color
    angles: Vector3
    style: str
    scale: Vector3


# Particle group


class ParticleSystemModel(VBLBaseModel):
    id: str = Field(alias="ID")
    n: int
    material: str = "circle"

    positions: list[Vector3] = Field(default_factory=list)
    sizes: list[float] = Field(default_factory=list)
    colors: list[Color] = Field(default_factory=list)


# Text


class TextModel(VBLBaseModel):
    id: str = Field(alias="ID")
    text: str
    color: Color = Color(r=0, g=0, b=0)
    font_size: int = 12
    position: Vector2 = Vector2()


# Custom meshes
class CustomMeshModel(VBLBaseModel):
    id: str = Field(alias="ID")
    vertices: list[Vector3]
    triangles: list[int]
    normals: list[Vector3] = None
    position: Vector3 = Vector3(x=0, y=0, z=0)
    use_reference: bool = True
    scale: Vector3 = Vector3(x=1, y=1, z=1)


# Volumes


class VolumeMetaModel(VBLBaseModel):
    name: str
    n_bytes: int
    colormap: list[Color]
    visible: bool


class VolumeDataChunk(VBLBaseModel):
    name: str
    bytes: str


# Utilities


class ColormapModel(VBLBaseModel):
    name: str = ""
    min: float = 0
    max: float = 1
