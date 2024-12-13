"""SystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7718

_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections", "SystemDeflection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2739
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7434,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7724,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2866,
        _2918,
        _2923,
    )
    from mastapy._private.system_model.fe import _2465

    Self = TypeVar("Self", bound="SystemDeflection")
    CastSelf = TypeVar("CastSelf", bound="SystemDeflection._Cast_SystemDeflection")


__docformat__ = "restructuredtext en"
__all__ = ("SystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemDeflection:
    """Special nested class for casting SystemDeflection to subclasses."""

    __parent__: "SystemDeflection"

    @property
    def fe_analysis(self: "CastSelf") -> "_7718.FEAnalysis":
        return self.__parent__._cast(_7718.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7724.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7724,
        )

        return self.__parent__._cast(_7724.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7709.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2739.Context":
        from mastapy._private.system_model.analyses_and_results import _2739

        return self.__parent__._cast(_2739.Context)

    @property
    def torsional_system_deflection(
        self: "CastSelf",
    ) -> "_2923.TorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2923,
        )

        return self.__parent__._cast(_2923.TorsionalSystemDeflection)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7434.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7434,
        )

        return self.__parent__._cast(_7434.AdvancedSystemDeflectionSubAnalysis)

    @property
    def system_deflection(self: "CastSelf") -> "SystemDeflection":
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
class SystemDeflection(_7718.FEAnalysis):
    """SystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def current_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentTime")

        if temp is None:
            return 0.0

        return temp

    @current_time.setter
    @enforce_parameter_types
    def current_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentTime", float(value) if value is not None else 0.0
        )

    @property
    def include_twist_in_misalignments(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTwistInMisalignments")

        if temp is None:
            return False

        return temp

    @include_twist_in_misalignments.setter
    @enforce_parameter_types
    def include_twist_in_misalignments(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTwistInMisalignments",
            bool(value) if value is not None else False,
        )

    @property
    def iterations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Iterations")

        if temp is None:
            return 0

        return temp

    @property
    def largest_power_across_a_connection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestPowerAcrossAConnection")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_circulating_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumCirculatingPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def power_convergence_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerConvergenceError")

        if temp is None:
            return 0.0

        return temp

    @property
    def power_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerError")

        if temp is None:
            return 0.0

        return temp

    @property
    def power_lost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLost")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_input_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalInputPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_load_dependent_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLoadDependentPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_speed_dependent_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalSpeedDependentPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_options(self: "Self") -> "_2918.SystemDeflectionOptions":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflectionOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def overall_efficiency_results(
        self: "Self",
    ) -> "_2866.LoadCaseOverallEfficiencyResult":
        """mastapy.system_model.analyses_and_results.system_deflections.LoadCaseOverallEfficiencyResult

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallEfficiencyResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bearing_race_f_es(self: "Self") -> "List[_2465.RaceBearingFESystemDeflection]":
        """List[mastapy.system_model.fe.RaceBearingFESystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingRaceFEs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_SystemDeflection
        """
        return _Cast_SystemDeflection(self)
