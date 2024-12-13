"""ParametricStudyDOEResultVariable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility.optimisation import _1604

_PARAMETRIC_STUDY_DOE_RESULT_VARIABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyDOEResultVariable",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility.optimisation import _1605

    Self = TypeVar("Self", bound="ParametricStudyDOEResultVariable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParametricStudyDOEResultVariable._Cast_ParametricStudyDOEResultVariable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyDOEResultVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyDOEResultVariable:
    """Special nested class for casting ParametricStudyDOEResultVariable to subclasses."""

    __parent__: "ParametricStudyDOEResultVariable"

    @property
    def pareto_optimisation_variable_base(
        self: "CastSelf",
    ) -> "_1604.ParetoOptimisationVariableBase":
        return self.__parent__._cast(_1604.ParetoOptimisationVariableBase)

    @property
    def parametric_study_doe_result_variable(
        self: "CastSelf",
    ) -> "ParametricStudyDOEResultVariable":
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
class ParametricStudyDOEResultVariable(_1604.ParetoOptimisationVariableBase):
    """ParametricStudyDOEResultVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_DOE_RESULT_VARIABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def entity_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EntityName")

        if temp is None:
            return ""

        return temp

    @property
    def max(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Max")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @max.setter
    @enforce_parameter_types
    def max(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Max", value)

    @property
    def min(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Min")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @min.setter
    @enforce_parameter_types
    def min(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Min", value)

    @property
    def parameter_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterName")

        if temp is None:
            return ""

        return temp

    @property
    def target_for_dominant_candidate_search(
        self: "Self",
    ) -> "_1605.PropertyTargetForDominantCandidateSearch":
        """mastapy.math_utility.optimisation.PropertyTargetForDominantCandidateSearch"""
        temp = pythonnet_property_get(self.wrapped, "TargetForDominantCandidateSearch")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.Optimisation.PropertyTargetForDominantCandidateSearch",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.optimisation._1605",
            "PropertyTargetForDominantCandidateSearch",
        )(value)

    @target_for_dominant_candidate_search.setter
    @enforce_parameter_types
    def target_for_dominant_candidate_search(
        self: "Self", value: "_1605.PropertyTargetForDominantCandidateSearch"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.MathUtility.Optimisation.PropertyTargetForDominantCandidateSearch",
        )
        pythonnet_property_set(self.wrapped, "TargetForDominantCandidateSearch", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyDOEResultVariable":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyDOEResultVariable
        """
        return _Cast_ParametricStudyDOEResultVariable(self)
