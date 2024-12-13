"""ThreeDViewContourOptionSecondSelection"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_THREE_D_VIEW_CONTOUR_OPTION_SECOND_SELECTION = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "ThreeDViewContourOptionSecondSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThreeDViewContourOptionSecondSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThreeDViewContourOptionSecondSelection._Cast_ThreeDViewContourOptionSecondSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDViewContourOptionSecondSelection",)


class ThreeDViewContourOptionSecondSelection(Enum):
    """ThreeDViewContourOptionSecondSelection

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _THREE_D_VIEW_CONTOUR_OPTION_SECOND_SELECTION

    PER_COMPONENT = 0
    PER_ELEMENT = 1
    ANGULAR_MAGNITUDE = 2
    RADIAL_TILT_MAGNITUDE = 3
    TWIST = 4
    LINEAR_MAGNITUDE = 5
    RADIAL_MAGNITUDE = 6
    AXIAL = 7
    LOCAL_X = 8
    LOCAL_Y = 9
    LOCAL_Z = 10
    TORQUE = 11
    NOMINAL_AXIAL = 12
    NOMINAL_BENDING = 13
    NOMINAL_TORSIONAL = 14
    NOMINAL_VON_MISES_ALTERNATING = 15
    NOMINAL_VON_MISES_MAX = 16
    NOMINAL_VON_MISES_MEAN = 17
    NOMINAL_MAXIMUM_PRINCIPAL = 18
    NOMINAL_MINIMUM_PRINCIPAL = 19
    NORMAL_DISPLACEMENT = 20
    NORMAL_VELOCITY = 21
    NORMAL_ACCELERATION = 22


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ThreeDViewContourOptionSecondSelection.__setattr__ = __enum_setattr
ThreeDViewContourOptionSecondSelection.__delattr__ = __enum_delattr
