from vbl_aquarium.utils.vbl_base_model import VBLBaseModel


class LogError(VBLBaseModel):
    msg: str


class LogWarning(VBLBaseModel):
    msg: str


class Log(VBLBaseModel):
    msg: str
