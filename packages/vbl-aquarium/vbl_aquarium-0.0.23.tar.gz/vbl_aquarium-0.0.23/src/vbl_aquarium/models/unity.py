from pydantic import BaseModel, Field

# Unity models don't get generated as .cs files since they exist in UnityEngine


class Color(BaseModel):
    r: float = Field(default=1, ge=0, le=1)
    g: float = Field(default=1, ge=0, le=1)
    b: float = Field(default=1, ge=0, le=1)
    a: float = Field(default=1, ge=0, le=1)


class Vector2(BaseModel):
    x: float = 0.0
    y: float = 0.0


class Vector3(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Vector4(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    def __add__(self, other):
        if isinstance(other, Vector4):
            return Vector4(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z, w=self.w + other.w)
        error = f"unsupported operand type(s) for +: 'Vector4' and '{type(other)}'"
        raise TypeError(error)

    def __sub__(self, other):
        if isinstance(other, Vector4):
            return Vector4(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z, w=self.w - other.w)
        error = f"unsupported operand type(s) for -: 'Vector4' and '{type(other)}'"
        raise TypeError(error)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector4(x=self.x * other, y=self.y * other, z=self.z * other, w=self.w * other)
        error = f"unsupported operand type(s) for *: 'Vector4' and '{type(other)}'"
        raise TypeError(error)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector4(x=self.x / other, y=self.y / other, z=self.z / other, w=self.w / other)
        error = f"unsupported operand type(s) for /: 'Vector4' and '{type(other)}'"
        raise TypeError(error)
