"""CylindricalGearPlungeShaver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters import _740

_CYLINDRICAL_GEAR_PLUNGE_SHAVER = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearPlungeShaver",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _638
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _731,
        _738,
        _743,
    )
    from mastapy._private.utility.databases import _1884

    Self = TypeVar("Self", bound="CylindricalGearPlungeShaver")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPlungeShaver._Cast_CylindricalGearPlungeShaver",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPlungeShaver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPlungeShaver:
    """Special nested class for casting CylindricalGearPlungeShaver to subclasses."""

    __parent__: "CylindricalGearPlungeShaver"

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_740.CylindricalGearShaver":
        return self.__parent__._cast(_740.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_743.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _743

        return self.__parent__._cast(_743.InvoluteCutterDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_738.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _738

        return self.__parent__._cast(_738.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_731.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _731

        return self.__parent__._cast(_731.CylindricalGearAbstractCutterDesign)

    @property
    def named_database_item(self: "CastSelf") -> "_1884.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.NamedDatabaseItem)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "CylindricalGearPlungeShaver":
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
class CylindricalGearPlungeShaver(_740.CylindricalGearShaver):
    """CylindricalGearPlungeShaver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PLUNGE_SHAVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def has_tolerances(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasTolerances")

        if temp is None:
            return False

        return temp

    @has_tolerances.setter
    @enforce_parameter_types
    def has_tolerances(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasTolerances", bool(value) if value is not None else False
        )

    @property
    def left_flank_micro_geometry(
        self: "Self",
    ) -> "_638.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank_micro_geometry(
        self: "Self",
    ) -> "_638.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def micro_geometry(
        self: "Self",
    ) -> "List[_638.CylindricalGearSpecifiedMicroGeometry]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPlungeShaver":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPlungeShaver
        """
        return _Cast_CylindricalGearPlungeShaver(self)
