"""CouplingLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7107

_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740, _2742, _2746
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6959,
        _6987,
        _6993,
        _7083,
        _7086,
        _7113,
        _7128,
    )
    from mastapy._private.system_model.part_model.couplings import _2646

    Self = TypeVar("Self", bound="CouplingLoadCase")
    CastSelf = TypeVar("CastSelf", bound="CouplingLoadCase._Cast_CouplingLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingLoadCase:
    """Special nested class for casting CouplingLoadCase to subclasses."""

    __parent__: "CouplingLoadCase"

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7107.SpecialisedAssemblyLoadCase":
        return self.__parent__._cast(_7107.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7083.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2746

        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def clutch_load_case(self: "CastSelf") -> "_6987.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ClutchLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6993.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6993,
        )

        return self.__parent__._cast(_6993.ConceptCouplingLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7086.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7086,
        )

        return self.__parent__._cast(_7086.PartToPartShearCouplingLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7113.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7113,
        )

        return self.__parent__._cast(_7113.SpringDamperLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7128.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7128,
        )

        return self.__parent__._cast(_7128.TorqueConverterLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "CouplingLoadCase":
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
class CouplingLoadCase(_7107.SpecialisedAssemblyLoadCase):
    """CouplingLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2646.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CouplingLoadCase
        """
        return _Cast_CouplingLoadCase(self)
