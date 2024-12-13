"""MicroGeometryDesignSpaceSearchCandidate"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_set_pareto_optimiser import _932
from mastapy._private.gears.ltca.cylindrical import _885

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "MicroGeometryDesignSpaceSearchCandidate",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1141

    Self = TypeVar("Self", bound="MicroGeometryDesignSpaceSearchCandidate")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryDesignSpaceSearchCandidate._Cast_MicroGeometryDesignSpaceSearchCandidate",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryDesignSpaceSearchCandidate",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryDesignSpaceSearchCandidate:
    """Special nested class for casting MicroGeometryDesignSpaceSearchCandidate to subclasses."""

    __parent__: "MicroGeometryDesignSpaceSearchCandidate"

    @property
    def design_space_search_candidate_base(
        self: "CastSelf",
    ) -> "_932.DesignSpaceSearchCandidateBase":
        pass

        return self.__parent__._cast(_932.DesignSpaceSearchCandidateBase)

    @property
    def micro_geometry_design_space_search_candidate(
        self: "CastSelf",
    ) -> "MicroGeometryDesignSpaceSearchCandidate":
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
class MicroGeometryDesignSpaceSearchCandidate(
    _932.DesignSpaceSearchCandidateBase[
        _885.CylindricalGearSetLoadDistributionAnalysis,
        "MicroGeometryDesignSpaceSearchCandidate",
    ]
):
    """MicroGeometryDesignSpaceSearchCandidate

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def candidate(self: "Self") -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Candidate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def candidate_for_slider(self: "Self") -> "_1141.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateForSlider")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def add_design(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddDesign")

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryDesignSpaceSearchCandidate":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryDesignSpaceSearchCandidate
        """
        return _Cast_MicroGeometryDesignSpaceSearchCandidate(self)
