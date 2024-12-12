from __future__ import annotations

from pydantic import Field

from vbl_aquarium.models.unity import Vector3, Vector4
from vbl_aquarium.utils.vbl_base_model import VBLBaseModel


class EphysLinkOptions(VBLBaseModel):
    """Options for running Ephys Link.

    :param background: Whether to skip the GUI and run using CLI arguments.
    :type background: bool
    :param ignore_updates: Whether to ignore updates.
    :type ignore_updates: bool
    :param type: Type of manipulator platform to use.
    :type type: str
    :param debug: Whether to print debug messages.
    :type debug: bool
    :param use_proxy: Whether to use VBL proxy service.
    :type use_proxy: bool
    :param proxy_address: Address of the proxy service.
    :type proxy_address: str
    :param mpm_port: Port for New Scale MPM HTTP server.
    :type mpm_port: int
    :param serial: Serial port for emergency stop.
    :type serial: str
    """

    background: bool = False
    ignore_updates: bool = False
    type: str = "ump-4"
    debug: bool = False
    use_proxy: bool = False
    proxy_address: str = "proxy2.virtualbrainlab.org"
    mpm_port: int = Field(default=8080, ge=1024, le=49151)
    serial: str = "no-e-stop"


class SetPositionRequest(VBLBaseModel):
    """Request format for moving a manipulator to a position.

    :param manipulator_id: ID of the manipulator to move.
    :type manipulator_id: str
    :param position: Position to move to in mm (X, Y, Z, W).
    :type position: Vector4
    :param speed: Speed to move at in mm/s.
    :type speed: float
    """

    manipulator_id: str = Field(min_length=1)
    position: Vector4
    speed: float = Field(gt=0)


class SetInsideBrainRequest(VBLBaseModel):
    """Request format for setting inside brain state.

    :param manipulator_id: ID of the manipulator to move.
    :type manipulator_id: str
    :param inside: Whether the manipulator is inside the brain.
    :type inside: bool
    """

    manipulator_id: str = Field(min_length=1)
    inside: bool


class SetDepthRequest(VBLBaseModel):
    """Request format for driving a manipulator to depth.

    :param manipulator_id: ID of the manipulator to move.
    :type manipulator_id: str
    :param depth: Depth to drive to in mm.
    :type depth: float
    :param speed: Speed to drive at in mm/s.
    :type speed: float
    """

    manipulator_id: str = Field(min_length=1)
    depth: float
    speed: float = Field(gt=0)


class GetManipulatorsResponse(VBLBaseModel):
    """Response format for requesting available manipulators.

    :param manipulators: List of manipulators.
    :type manipulators: list[str]
    :param num_axes: Number of axes for the manipulators.
    :type num_axes: int
    :param dimensions: Dimensions of the manipulators (3-axis manipulators should set w to 0).
    :type dimensions: Vector4
    :param error: Error message if any.
    :type error: str
    """

    manipulators: list[str] = Field(default_factory=list)
    num_axes: int = Field(default=0, ge=-1)
    dimensions: Vector4 = Vector4()
    error: str = ""


class PositionalResponse(VBLBaseModel):
    """Response format for the manipulator position.

    :param position: Position of the manipulator.
    :type position: Vector4
    :param error: Error message if any.
    :type error: str
    """

    position: Vector4 = Vector4()
    error: str = ""


class AngularResponse(VBLBaseModel):
    """Response format for the manipulator angles.

    :param angles: Position of the manipulator.
    :type angles: Vector3
    """

    angles: Vector3 = Vector3()
    error: str = ""


class ShankCountResponse(VBLBaseModel):
    """Response format for the shank count.

    :param shank_count: Number of shanks.
    :type shank_count: int
    :param error: Error message if any.
    :type error: str
    """

    shank_count: int = Field(default=1, ge=1)
    error: str = ""


class SetDepthResponse(VBLBaseModel):
    """Response format for driving a manipulator to depth.

    :param depth: Depth the manipulator is at in mm.
    :type depth: float
    :param error: Error message if any.
    :type error: str
    """

    depth: float = 0
    error: str = ""


class BooleanStateResponse(VBLBaseModel):
    """Response format for a boolean state.

    :param state: State of the event.
    :type state: bool
    :param error: Error message if any.
    :type error: str
    """

    state: bool = False
    error: str = ""
