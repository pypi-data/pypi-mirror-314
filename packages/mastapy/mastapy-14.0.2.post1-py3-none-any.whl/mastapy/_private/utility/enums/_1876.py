"""ThreeDViewContourOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_THREE_D_VIEW_CONTOUR_OPTION = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "ThreeDViewContourOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThreeDViewContourOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ThreeDViewContourOption._Cast_ThreeDViewContourOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDViewContourOption",)


class ThreeDViewContourOption(Enum):
    """ThreeDViewContourOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _THREE_D_VIEW_CONTOUR_OPTION

    NO_CONTOUR = 0
    STRAIN_ENERGY_PER_COMPONENT = 1
    KINETIC_ENERGY_PER_COMPONENT = 2
    STRAIN_ENERGY_PER_ELEMENT = 3
    KINETIC_ENERGY_PER_ELEMENT = 4
    DISPLACEMENT_ANGULAR_MAGNITUDE = 5
    DISPLACEMENT_RADIAL_TILT_MAGNITUDE = 6
    DISPLACEMENT_TWIST = 7
    DISPLACEMENT_LINEAR_MAGNITUDE = 8
    DISPLACEMENT_RADIAL_MAGNITUDE = 9
    DISPLACEMENT_AXIAL = 10
    DISPLACEMENT_LOCAL_X = 11
    DISPLACEMENT_LOCAL_Y = 12
    DISPLACEMENT_LOCAL_Z = 13
    FORCE_ANGULAR_MAGNITUDE = 14
    FORCE_TORQUE = 15
    FORCE_LINEAR_MAGNITUDE = 16
    FORCE_RADIAL_MAGNITUDE = 17
    FORCE_AXIAL = 18
    STRESS_NOMINAL_AXIAL = 19
    STRESS_NOMINAL_BENDING = 20
    STRESS_NOMINAL_TORSIONAL = 21
    STRESS_NOMINAL_VON_MISES_ALTERNATING = 22
    STRESS_NOMINAL_VON_MISES_MAX = 23
    STRESS_NOMINAL_VON_MISES_MEAN = 24
    STRESS_NOMINAL_MAXIMUM_PRINCIPAL = 25
    STRESS_NOMINAL_MINIMUM_PRINCIPAL = 26
    FE_MESH_NORMAL_DISPLACEMENT = 27
    FE_MESH_NORMAL_VELOCITY = 28
    FE_MESH_NORMAL_ACCELERATION = 29
    SOUND_PRESSURE = 30


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ThreeDViewContourOption.__setattr__ = __enum_setattr
ThreeDViewContourOption.__delattr__ = __enum_delattr
