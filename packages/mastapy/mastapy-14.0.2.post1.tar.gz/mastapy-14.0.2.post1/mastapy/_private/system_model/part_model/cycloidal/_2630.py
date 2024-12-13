"""CycloidalDisc"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2493

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.cycloidal import _1504
    from mastapy._private.materials import _282
    from mastapy._private.system_model import _2260
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2396
    from mastapy._private.system_model.part_model import _2494, _2502, _2519, _2528

    Self = TypeVar("Self", bound="CycloidalDisc")
    CastSelf = TypeVar("CastSelf", bound="CycloidalDisc._Cast_CycloidalDisc")


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDisc",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDisc:
    """Special nested class for casting CycloidalDisc to subclasses."""

    __parent__: "CycloidalDisc"

    @property
    def abstract_shaft(self: "CastSelf") -> "_2493.AbstractShaft":
        return self.__parent__._cast(_2493.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2494.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2494

        return self.__parent__._cast(_2494.AbstractShaftOrHousing)

    @property
    def component(self: "CastSelf") -> "_2502.Component":
        from mastapy._private.system_model.part_model import _2502

        return self.__parent__._cast(_2502.Component)

    @property
    def part(self: "CastSelf") -> "_2528.Part":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2260.DesignEntity":
        from mastapy._private.system_model import _2260

        return self.__parent__._cast(_2260.DesignEntity)

    @property
    def cycloidal_disc(self: "CastSelf") -> "CycloidalDisc":
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
class CycloidalDisc(_2493.AbstractShaft):
    """CycloidalDisc

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bore_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoreDiameter")

        if temp is None:
            return 0.0

        return temp

    @bore_diameter.setter
    @enforce_parameter_types
    def bore_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BoreDiameter", float(value) if value is not None else 0.0
        )

    @property
    def disc_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DiscMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @disc_material_database.setter
    @enforce_parameter_types
    def disc_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DiscMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def hole_diameter_for_eccentric_bearing(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HoleDiameterForEccentricBearing")

        if temp is None:
            return 0.0

        return temp

    @hole_diameter_for_eccentric_bearing.setter
    @enforce_parameter_types
    def hole_diameter_for_eccentric_bearing(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HoleDiameterForEccentricBearing",
            float(value) if value is not None else 0.0,
        )

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def number_of_planetary_sockets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanetarySockets")

        if temp is None:
            return 0

        return temp

    @number_of_planetary_sockets.setter
    @enforce_parameter_types
    def number_of_planetary_sockets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPlanetarySockets",
            int(value) if value is not None else 0,
        )

    @property
    def cycloidal_disc_design(self: "Self") -> "_1504.CycloidalDiscDesign":
        """mastapy.cycloidal.CycloidalDiscDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def disc_material(self: "Self") -> "_282.Material":
        """mastapy.materials.Material

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiscMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def load_sharing_settings(self: "Self") -> "_2519.LoadSharingSettings":
        """mastapy.system_model.part_model.LoadSharingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetary_bearing_sockets(
        self: "Self",
    ) -> "List[_2396.CycloidalDiscPlanetaryBearingSocket]":
        """List[mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingSocket]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryBearingSockets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDisc":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDisc
        """
        return _Cast_CycloidalDisc(self)
