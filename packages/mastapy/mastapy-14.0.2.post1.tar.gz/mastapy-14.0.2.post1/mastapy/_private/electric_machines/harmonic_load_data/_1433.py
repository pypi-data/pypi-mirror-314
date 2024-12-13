"""SpeedDependentHarmonicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1430

_SPEED_DEPENDENT_HARMONIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "SpeedDependentHarmonicLoadData"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1428
    from mastapy._private.electric_machines.results import _1371
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7024,
        _7025,
        _7026,
        _7027,
        _7028,
        _7029,
        _7030,
        _7092,
        _7134,
    )

    Self = TypeVar("Self", bound="SpeedDependentHarmonicLoadData")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpeedDependentHarmonicLoadData._Cast_SpeedDependentHarmonicLoadData",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpeedDependentHarmonicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpeedDependentHarmonicLoadData:
    """Special nested class for casting SpeedDependentHarmonicLoadData to subclasses."""

    __parent__: "SpeedDependentHarmonicLoadData"

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1430.HarmonicLoadDataBase":
        return self.__parent__._cast(_1430.HarmonicLoadDataBase)

    @property
    def dynamic_force_results(self: "CastSelf") -> "_1371.DynamicForceResults":
        from mastapy._private.electric_machines.results import _1371

        return self.__parent__._cast(_1371.DynamicForceResults)

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1428.ElectricMachineHarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1428

        return self.__parent__._cast(_1428.ElectricMachineHarmonicLoadDataBase)

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7024.ElectricMachineHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7024,
        )

        return self.__parent__._cast(_7024.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_from_excel(
        self: "CastSelf",
    ) -> "_7025.ElectricMachineHarmonicLoadDataFromExcel":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7025,
        )

        return self.__parent__._cast(_7025.ElectricMachineHarmonicLoadDataFromExcel)

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
    def electric_machine_harmonic_load_data_from_masta(
        self: "CastSelf",
    ) -> "_7028.ElectricMachineHarmonicLoadDataFromMASTA":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7028,
        )

        return self.__parent__._cast(_7028.ElectricMachineHarmonicLoadDataFromMASTA)

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
    ) -> "_7030.ElectricMachineHarmonicLoadDataFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7030,
        )

        return self.__parent__._cast(
            _7030.ElectricMachineHarmonicLoadDataFromMotorPackages
        )

    @property
    def point_load_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7092.PointLoadHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7092,
        )

        return self.__parent__._cast(_7092.PointLoadHarmonicLoadData)

    @property
    def unbalanced_mass_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7134.UnbalancedMassHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7134,
        )

        return self.__parent__._cast(_7134.UnbalancedMassHarmonicLoadData)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "SpeedDependentHarmonicLoadData":
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
class SpeedDependentHarmonicLoadData(_1430.HarmonicLoadDataBase):
    """SpeedDependentHarmonicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPEED_DEPENDENT_HARMONIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def selected_speed(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_float":
        """ListWithSelectedItem[float]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedSpeed")

        if temp is None:
            return 0.0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_float",
        )(temp)

    @selected_speed.setter
    @enforce_parameter_types
    def selected_speed(self: "Self", value: "float") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_float.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0
        )
        pythonnet_property_set(self.wrapped, "SelectedSpeed", value)

    @property
    def show_all_speeds(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllSpeeds")

        if temp is None:
            return False

        return temp

    @show_all_speeds.setter
    @enforce_parameter_types
    def show_all_speeds(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllSpeeds", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SpeedDependentHarmonicLoadData":
        """Cast to another type.

        Returns:
            _Cast_SpeedDependentHarmonicLoadData
        """
        return _Cast_SpeedDependentHarmonicLoadData(self)
