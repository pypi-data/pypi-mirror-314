"""ElectricMachineStatorToothTangentialLoadsExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5876

_ELECTRIC_MACHINE_STATOR_TOOTH_TANGENTIAL_LOADS_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ElectricMachineStatorToothTangentialLoadsExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5815,
        _5869,
        _5930,
    )

    Self = TypeVar(
        "Self", bound="ElectricMachineStatorToothTangentialLoadsExcitationDetail"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineStatorToothTangentialLoadsExcitationDetail._Cast_ElectricMachineStatorToothTangentialLoadsExcitationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineStatorToothTangentialLoadsExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineStatorToothTangentialLoadsExcitationDetail:
    """Special nested class for casting ElectricMachineStatorToothTangentialLoadsExcitationDetail to subclasses."""

    __parent__: "ElectricMachineStatorToothTangentialLoadsExcitationDetail"

    @property
    def electric_machine_stator_tooth_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_5876.ElectricMachineStatorToothLoadsExcitationDetail":
        return self.__parent__._cast(
            _5876.ElectricMachineStatorToothLoadsExcitationDetail
        )

    @property
    def electric_machine_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5869.ElectricMachinePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5869,
        )

        return self.__parent__._cast(_5869.ElectricMachinePeriodicExcitationDetail)

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_5930.PeriodicExcitationWithReferenceShaft":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5930,
        )

        return self.__parent__._cast(_5930.PeriodicExcitationWithReferenceShaft)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5815.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5815,
        )

        return self.__parent__._cast(_5815.AbstractPeriodicExcitationDetail)

    @property
    def electric_machine_stator_tooth_tangential_loads_excitation_detail(
        self: "CastSelf",
    ) -> "ElectricMachineStatorToothTangentialLoadsExcitationDetail":
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
class ElectricMachineStatorToothTangentialLoadsExcitationDetail(
    _5876.ElectricMachineStatorToothLoadsExcitationDetail
):
    """ElectricMachineStatorToothTangentialLoadsExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ELECTRIC_MACHINE_STATOR_TOOTH_TANGENTIAL_LOADS_EXCITATION_DETAIL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ElectricMachineStatorToothTangentialLoadsExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineStatorToothTangentialLoadsExcitationDetail
        """
        return _Cast_ElectricMachineStatorToothTangentialLoadsExcitationDetail(self)
