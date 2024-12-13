"""PlungeShavingDynamicsViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _780,
    _795,
)

_PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "PlungeShavingDynamicsViewModel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _653
    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _781,
        _796,
    )

    Self = TypeVar("Self", bound="PlungeShavingDynamicsViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlungeShavingDynamicsViewModel._Cast_PlungeShavingDynamicsViewModel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShavingDynamicsViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShavingDynamicsViewModel:
    """Special nested class for casting PlungeShavingDynamicsViewModel to subclasses."""

    __parent__: "PlungeShavingDynamicsViewModel"

    @property
    def shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_795.ShavingDynamicsViewModel":
        return self.__parent__._cast(_795.ShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model_base(
        self: "CastSelf",
    ) -> "_796.ShavingDynamicsViewModelBase":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _796,
        )

        return self.__parent__._cast(_796.ShavingDynamicsViewModelBase)

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "_653.GearManufacturingConfigurationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical import _653

        return self.__parent__._cast(_653.GearManufacturingConfigurationViewModel)

    @property
    def plunge_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "PlungeShavingDynamicsViewModel":
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
class PlungeShavingDynamicsViewModel(
    _795.ShavingDynamicsViewModel[_780.PlungeShaverDynamics]
):
    """PlungeShavingDynamicsViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def transverse_plane_on_gear_for_analysis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TransversePlaneOnGearForAnalysis")

        if temp is None:
            return 0.0

        return temp

    @transverse_plane_on_gear_for_analysis.setter
    @enforce_parameter_types
    def transverse_plane_on_gear_for_analysis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransversePlaneOnGearForAnalysis",
            float(value) if value is not None else 0.0,
        )

    @property
    def settings(self: "Self") -> "_781.PlungeShaverDynamicSettings":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlungeShavingDynamicsViewModel":
        """Cast to another type.

        Returns:
            _Cast_PlungeShavingDynamicsViewModel
        """
        return _Cast_PlungeShavingDynamicsViewModel(self)
