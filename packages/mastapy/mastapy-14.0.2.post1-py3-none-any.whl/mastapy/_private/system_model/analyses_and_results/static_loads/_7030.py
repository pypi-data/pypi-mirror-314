"""ElectricMachineHarmonicLoadDataFromMotorPackages"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7024

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_PACKAGES = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadDataFromMotorPackages",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.electric_machines.harmonic_load_data import (
        _1428,
        _1430,
        _1433,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7026,
        _7027,
        _7029,
        _7033,
    )

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadDataFromMotorPackages")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadDataFromMotorPackages._Cast_ElectricMachineHarmonicLoadDataFromMotorPackages",
    )

T = TypeVar("T", bound="_7033.ElectricMachineHarmonicLoadImportOptionsBase")

__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadDataFromMotorPackages",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadDataFromMotorPackages:
    """Special nested class for casting ElectricMachineHarmonicLoadDataFromMotorPackages to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadDataFromMotorPackages"

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7024.ElectricMachineHarmonicLoadData":
        return self.__parent__._cast(_7024.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1428.ElectricMachineHarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1428

        return self.__parent__._cast(_1428.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1433.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1433

        return self.__parent__._cast(_1433.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1430.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1430

        return self.__parent__._cast(_1430.HarmonicLoadDataBase)

    @property
    def electric_machine_harmonic_load_data_from_flux(
        self: "CastSelf",
    ) -> "_7026.ElectricMachineHarmonicLoadDataFromFlux":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7026,
        )

        return self.__parent__._cast(_7026.ElectricMachineHarmonicLoadDataFromFlux)

    @property
    def electric_machine_harmonic_load_data_from_jmag(
        self: "CastSelf",
    ) -> "_7027.ElectricMachineHarmonicLoadDataFromJMAG":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7027,
        )

        return self.__parent__._cast(_7027.ElectricMachineHarmonicLoadDataFromJMAG)

    @property
    def electric_machine_harmonic_load_data_from_motor_cad(
        self: "CastSelf",
    ) -> "_7029.ElectricMachineHarmonicLoadDataFromMotorCAD":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7029,
        )

        return self.__parent__._cast(_7029.ElectricMachineHarmonicLoadDataFromMotorCAD)

    @property
    def electric_machine_harmonic_load_data_from_motor_packages(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadDataFromMotorPackages":
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
class ElectricMachineHarmonicLoadDataFromMotorPackages(
    _7024.ElectricMachineHarmonicLoadData, Generic[T]
):
    """ElectricMachineHarmonicLoadDataFromMotorPackages

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_PACKAGES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ElectricMachineHarmonicLoadDataFromMotorPackages":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadDataFromMotorPackages
        """
        return _Cast_ElectricMachineHarmonicLoadDataFromMotorPackages(self)
