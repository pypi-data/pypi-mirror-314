"""ParetoOptimisationInput"""

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
from mastapy._private.math_utility.optimisation import _1603

_PARETO_OPTIMISATION_INPUT = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationInput"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1539
    from mastapy._private.math_utility.optimisation import _1604, _1607

    Self = TypeVar("Self", bound="ParetoOptimisationInput")
    CastSelf = TypeVar(
        "CastSelf", bound="ParetoOptimisationInput._Cast_ParetoOptimisationInput"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationInput:
    """Special nested class for casting ParetoOptimisationInput to subclasses."""

    __parent__: "ParetoOptimisationInput"

    @property
    def pareto_optimisation_variable(
        self: "CastSelf",
    ) -> "_1603.ParetoOptimisationVariable":
        return self.__parent__._cast(_1603.ParetoOptimisationVariable)

    @property
    def pareto_optimisation_variable_base(
        self: "CastSelf",
    ) -> "_1604.ParetoOptimisationVariableBase":
        from mastapy._private.math_utility.optimisation import _1604

        return self.__parent__._cast(_1604.ParetoOptimisationVariableBase)

    @property
    def pareto_optimisation_input(self: "CastSelf") -> "ParetoOptimisationInput":
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
class ParetoOptimisationInput(_1603.ParetoOptimisationVariable):
    """ParetoOptimisationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_steps(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSteps")

        if temp is None:
            return 0

        return temp

    @number_of_steps.setter
    @enforce_parameter_types
    def number_of_steps(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSteps", int(value) if value is not None else 0
        )

    @property
    def range(self: "Self") -> "_1539.Range":
        """mastapy.math_utility.Range"""
        temp = pythonnet_property_get(self.wrapped, "Range")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @range.setter
    @enforce_parameter_types
    def range(self: "Self", value: "_1539.Range") -> None:
        pythonnet_property_set(self.wrapped, "Range", value.wrapped)

    @property
    def specify_input_range_as(self: "Self") -> "_1607.SpecifyOptimisationInputAs":
        """mastapy.math_utility.optimisation.SpecifyOptimisationInputAs"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyInputRangeAs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.Optimisation.SpecifyOptimisationInputAs"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.optimisation._1607",
            "SpecifyOptimisationInputAs",
        )(value)

    @specify_input_range_as.setter
    @enforce_parameter_types
    def specify_input_range_as(
        self: "Self", value: "_1607.SpecifyOptimisationInputAs"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.Optimisation.SpecifyOptimisationInputAs"
        )
        pythonnet_property_set(self.wrapped, "SpecifyInputRangeAs", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationInput":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationInput
        """
        return _Cast_ParetoOptimisationInput(self)
