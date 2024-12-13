"""InteriorPermanentMagnetAndSynchronousReluctanceRotor"""

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
from mastapy._private.electric_machines import _1337

_INTERIOR_PERMANENT_MAGNET_AND_SYNCHRONOUS_RELUCTANCE_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import (
        _1297,
        _1317,
        _1335,
        _1340,
        _1343,
        _1359,
        _1360,
        _1370,
    )

    Self = TypeVar("Self", bound="InteriorPermanentMagnetAndSynchronousReluctanceRotor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InteriorPermanentMagnetAndSynchronousReluctanceRotor._Cast_InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InteriorPermanentMagnetAndSynchronousReluctanceRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InteriorPermanentMagnetAndSynchronousReluctanceRotor:
    """Special nested class for casting InteriorPermanentMagnetAndSynchronousReluctanceRotor to subclasses."""

    __parent__: "InteriorPermanentMagnetAndSynchronousReluctanceRotor"

    @property
    def permanent_magnet_rotor(self: "CastSelf") -> "_1337.PermanentMagnetRotor":
        return self.__parent__._cast(_1337.PermanentMagnetRotor)

    @property
    def rotor(self: "CastSelf") -> "_1340.Rotor":
        from mastapy._private.electric_machines import _1340

        return self.__parent__._cast(_1340.Rotor)

    @property
    def wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "_1370.WoundFieldSynchronousRotor":
        from mastapy._private.electric_machines import _1370

        return self.__parent__._cast(_1370.WoundFieldSynchronousRotor)

    @property
    def interior_permanent_magnet_and_synchronous_reluctance_rotor(
        self: "CastSelf",
    ) -> "InteriorPermanentMagnetAndSynchronousReluctanceRotor":
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
class InteriorPermanentMagnetAndSynchronousReluctanceRotor(_1337.PermanentMagnetRotor):
    """InteriorPermanentMagnetAndSynchronousReluctanceRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERIOR_PERMANENT_MAGNET_AND_SYNCHRONOUS_RELUCTANCE_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def flux_barrier_style(self: "Self") -> "_1317.FluxBarrierStyle":
        """mastapy.electric_machines.FluxBarrierStyle"""
        temp = pythonnet_property_get(self.wrapped, "FluxBarrierStyle")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.FluxBarrierStyle"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1317", "FluxBarrierStyle"
        )(value)

    @flux_barrier_style.setter
    @enforce_parameter_types
    def flux_barrier_style(self: "Self", value: "_1317.FluxBarrierStyle") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.FluxBarrierStyle"
        )
        pythonnet_property_set(self.wrapped, "FluxBarrierStyle", value)

    @property
    def maximum_radius_of_curvature_for_flux_barrier_corners(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumRadiusOfCurvatureForFluxBarrierCorners"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_radius_of_curvature_for_flux_barrier_corners.setter
    @enforce_parameter_types
    def maximum_radius_of_curvature_for_flux_barrier_corners(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumRadiusOfCurvatureForFluxBarrierCorners",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_cooling_duct_layers(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCoolingDuctLayers")

        if temp is None:
            return 0

        return temp

    @number_of_cooling_duct_layers.setter
    @enforce_parameter_types
    def number_of_cooling_duct_layers(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCoolingDuctLayers",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_magnet_flux_barrier_layers(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfMagnetFluxBarrierLayers")

        if temp is None:
            return 0

        return temp

    @number_of_magnet_flux_barrier_layers.setter
    @enforce_parameter_types
    def number_of_magnet_flux_barrier_layers(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfMagnetFluxBarrierLayers",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_notch_specifications(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfNotchSpecifications")

        if temp is None:
            return 0

        return temp

    @number_of_notch_specifications.setter
    @enforce_parameter_types
    def number_of_notch_specifications(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfNotchSpecifications",
            int(value) if value is not None else 0,
        )

    @property
    def rotor_type(self: "Self") -> "_1343.RotorType":
        """mastapy.electric_machines.RotorType"""
        temp = pythonnet_property_get(self.wrapped, "RotorType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.RotorType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1343", "RotorType"
        )(value)

    @rotor_type.setter
    @enforce_parameter_types
    def rotor_type(self: "Self", value: "_1343.RotorType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.RotorType"
        )
        pythonnet_property_set(self.wrapped, "RotorType", value)

    @property
    def cooling_duct_layers(
        self: "Self",
    ) -> "List[_1297.CoolingDuctLayerSpecification]":
        """List[mastapy.electric_machines.CoolingDuctLayerSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoolingDuctLayers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def notch_specifications(self: "Self") -> "List[_1335.NotchSpecification]":
        """List[mastapy.electric_machines.NotchSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NotchSpecifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def u_shape_layers(self: "Self") -> "List[_1359.UShapedLayerSpecification]":
        """List[mastapy.electric_machines.UShapedLayerSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UShapeLayers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def v_shape_magnet_layers(
        self: "Self",
    ) -> "List[_1360.VShapedMagnetLayerSpecification]":
        """List[mastapy.electric_machines.VShapedMagnetLayerSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VShapeMagnetLayers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InteriorPermanentMagnetAndSynchronousReluctanceRotor":
        """Cast to another type.

        Returns:
            _Cast_InteriorPermanentMagnetAndSynchronousReluctanceRotor
        """
        return _Cast_InteriorPermanentMagnetAndSynchronousReluctanceRotor(self)
