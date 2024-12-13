"""CylindricalCutterSimulatableGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CYLINDRICAL_CUTTER_SIMULATABLE_GEAR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "CylindricalCutterSimulatableGear",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry.two_d import _324

    Self = TypeVar("Self", bound="CylindricalCutterSimulatableGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalCutterSimulatableGear._Cast_CylindricalCutterSimulatableGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalCutterSimulatableGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalCutterSimulatableGear:
    """Special nested class for casting CylindricalCutterSimulatableGear to subclasses."""

    __parent__: "CylindricalCutterSimulatableGear"

    @property
    def cylindrical_cutter_simulatable_gear(
        self: "CastSelf",
    ) -> "CylindricalCutterSimulatableGear":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class CylindricalCutterSimulatableGear(_0.APIBase):
    """CylindricalCutterSimulatableGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_CUTTER_SIMULATABLE_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def generating_profile_shift_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeneratingProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def helix_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def internal_external(self: "Self") -> "_324.InternalExternalType":
        """mastapy.geometry.two_d.InternalExternalType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalExternal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.geometry.two_d._324", "InternalExternalType"
        )(value)

    @property
    def is_left_handed(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLeftHanded")

        if temp is None:
            return False

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_teeth_unsigned(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethUnsigned")

        if temp is None:
            return 0.0

        return temp

    @property
    def reference_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalCutterSimulatableGear":
        """Cast to another type.

        Returns:
            _Cast_CylindricalCutterSimulatableGear
        """
        return _Cast_CylindricalCutterSimulatableGear(self)
