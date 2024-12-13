"""ContourDrawStyle"""

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
from mastapy._private.geometry import _320

_CONTOUR_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ContourDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6732,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6474,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5898,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5590
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4775
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4135
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3978,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3185,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2917,
    )
    from mastapy._private.system_model.drawing import _2309
    from mastapy._private.utility.enums import _1876
    from mastapy._private.utility_gui import _1906

    Self = TypeVar("Self", bound="ContourDrawStyle")
    CastSelf = TypeVar("CastSelf", bound="ContourDrawStyle._Cast_ContourDrawStyle")


__docformat__ = "restructuredtext en"
__all__ = ("ContourDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContourDrawStyle:
    """Special nested class for casting ContourDrawStyle to subclasses."""

    __parent__: "ContourDrawStyle"

    @property
    def draw_style_base(self: "CastSelf") -> "_320.DrawStyleBase":
        return self.__parent__._cast(_320.DrawStyleBase)

    @property
    def system_deflection_draw_style(
        self: "CastSelf",
    ) -> "_2917.SystemDeflectionDrawStyle":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2917,
        )

        return self.__parent__._cast(_2917.SystemDeflectionDrawStyle)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "CastSelf",
    ) -> "_3185.SteadyStateSynchronousResponseDrawStyle":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3185,
        )

        return self.__parent__._cast(_3185.SteadyStateSynchronousResponseDrawStyle)

    @property
    def stability_analysis_draw_style(
        self: "CastSelf",
    ) -> "_3978.StabilityAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3978,
        )

        return self.__parent__._cast(_3978.StabilityAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "_4135.RotorDynamicsDrawStyle":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4135,
        )

        return self.__parent__._cast(_4135.RotorDynamicsDrawStyle)

    @property
    def modal_analysis_draw_style(self: "CastSelf") -> "_4775.ModalAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4775,
        )

        return self.__parent__._cast(_4775.ModalAnalysisDrawStyle)

    @property
    def mbd_analysis_draw_style(self: "CastSelf") -> "_5590.MBDAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5590,
        )

        return self.__parent__._cast(_5590.MBDAnalysisDrawStyle)

    @property
    def harmonic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_5898.HarmonicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5898,
        )

        return self.__parent__._cast(_5898.HarmonicAnalysisDrawStyle)

    @property
    def dynamic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6474.DynamicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6474,
        )

        return self.__parent__._cast(_6474.DynamicAnalysisDrawStyle)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6732.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6732,
        )

        return self.__parent__._cast(_6732.CriticalSpeedAnalysisDrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "ContourDrawStyle":
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
class ContourDrawStyle(_320.DrawStyleBase):
    """ContourDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTOUR_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contour(self: "Self") -> "_1876.ThreeDViewContourOption":
        """mastapy.utility.enums.ThreeDViewContourOption"""
        temp = pythonnet_property_get(self.wrapped, "Contour")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.enums._1876", "ThreeDViewContourOption"
        )(value)

    @contour.setter
    @enforce_parameter_types
    def contour(self: "Self", value: "_1876.ThreeDViewContourOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )
        pythonnet_property_set(self.wrapped, "Contour", value)

    @property
    def minimum_peak_value_displacement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueDisplacement")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_displacement.setter
    @enforce_parameter_types
    def minimum_peak_value_displacement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueDisplacement",
            float(value) if value is not None else 0.0,
        )

    @property
    def minimum_peak_value_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueStress")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_stress.setter
    @enforce_parameter_types
    def minimum_peak_value_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def show_local_maxima(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowLocalMaxima")

        if temp is None:
            return False

        return temp

    @show_local_maxima.setter
    @enforce_parameter_types
    def show_local_maxima(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowLocalMaxima", bool(value) if value is not None else False
        )

    @property
    def deflection_scaling(self: "Self") -> "_1906.ScalingDrawStyle":
        """mastapy.utility_gui.ScalingDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeflectionScaling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def model_view_options(self: "Self") -> "_2309.ModelViewOptionsDrawStyle":
        """mastapy.system_model.drawing.ModelViewOptionsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelViewOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ContourDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_ContourDrawStyle
        """
        return _Cast_ContourDrawStyle(self)
