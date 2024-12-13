"""KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _427

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030",
    "KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _379
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _429

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating._Cast_KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating"

    @property
    def klingelnberg_conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_427.KlingelnbergConicalMeshSingleFlankRating":
        return self.__parent__._cast(_427.KlingelnbergConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_379.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _379

        return self.__parent__._cast(_379.MeshSingleFlankRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating":
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
class KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating(
    _427.KlingelnbergConicalMeshSingleFlankRating
):
    """KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_ratio_factor_scuffing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactorScuffing")

        if temp is None:
            return 0.0

        return temp

    @property
    def curvature_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def friction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def integral_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_distribution_factor_transverse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorTransverse")

        if temp is None:
            return 0.0

        return temp

    @property
    def relating_factor_for_the_thermal_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelatingFactorForTheThermalFlashTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tangential_speed_sum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialSpeedSum")

        if temp is None:
            return 0.0

        return temp

    @property
    def thermal_flash_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalFlashFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_429.KlingelnbergCycloPalloidConicalGearSingleFlankRating]":
        """List[mastapy.gears.rating.klingelnberg_conical.kn3030.KlingelnbergCycloPalloidConicalGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def kn3030_klingelnberg_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_429.KlingelnbergCycloPalloidConicalGearSingleFlankRating]":
        """List[mastapy.gears.rating.klingelnberg_conical.kn3030.KlingelnbergCycloPalloidConicalGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KN3030KlingelnbergGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating(self)
