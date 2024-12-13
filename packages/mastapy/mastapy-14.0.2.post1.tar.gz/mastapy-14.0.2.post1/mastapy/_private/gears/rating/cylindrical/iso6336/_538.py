"""ToothFlankFractureAnalysisContactPointCommon"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_COMMON = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureAnalysisContactPointCommon",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _537, _539, _541

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisContactPointCommon")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisContactPointCommon._Cast_ToothFlankFractureAnalysisContactPointCommon",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisContactPointCommon",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisContactPointCommon:
    """Special nested class for casting ToothFlankFractureAnalysisContactPointCommon to subclasses."""

    __parent__: "ToothFlankFractureAnalysisContactPointCommon"

    @property
    def tooth_flank_fracture_analysis_contact_point(
        self: "CastSelf",
    ) -> "_537.ToothFlankFractureAnalysisContactPoint":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _537

        return self.__parent__._cast(_537.ToothFlankFractureAnalysisContactPoint)

    @property
    def tooth_flank_fracture_analysis_contact_point_method_a(
        self: "CastSelf",
    ) -> "_539.ToothFlankFractureAnalysisContactPointMethodA":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _539

        return self.__parent__._cast(_539.ToothFlankFractureAnalysisContactPointMethodA)

    @property
    def tooth_flank_fracture_analysis_contact_point_common(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisContactPointCommon":
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
class ToothFlankFractureAnalysisContactPointCommon(_0.APIBase):
    """ToothFlankFractureAnalysisContactPointCommon

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_COMMON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def effective_case_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveCaseDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def half_of_hertzian_contact_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HalfOfHertzianContactWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def local_normal_radius_of_relative_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocalNormalRadiusOfRelativeCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def material_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def material_factor_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialFactorConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_material_exposure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumMaterialExposure")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_residual_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumResidualStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_thickness_at_the_diameter_corresponding_to_the_middle_between_b_and_d(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "TransverseThicknessAtTheDiameterCorrespondingToTheMiddleBetweenBAndD",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_point_with_maximum_local_material_exposure(
        self: "Self",
    ) -> "_541.ToothFlankFractureAnalysisPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AnalysisPointWithMaximumLocalMaterialExposure"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def watch_points(self: "Self") -> "List[_541.ToothFlankFractureAnalysisPoint]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WatchPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisContactPointCommon":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisContactPointCommon
        """
        return _Cast_ToothFlankFractureAnalysisContactPointCommon(self)
