"""VirtualCylindricalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_VIRTUAL_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears", "VirtualCylindricalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.rating.virtual_cylindrical_gears import (
        _392,
        _393,
        _395,
        _396,
        _400,
        _402,
        _406,
        _407,
    )

    Self = TypeVar("Self", bound="VirtualCylindricalGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="VirtualCylindricalGearSet._Cast_VirtualCylindricalGearSet"
    )

T = TypeVar("T", bound="_402.VirtualCylindricalGearBasic")

__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearSet:
    """Special nested class for casting VirtualCylindricalGearSet to subclasses."""

    __parent__: "VirtualCylindricalGearSet"

    @property
    def bevel_virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_392.BevelVirtualCylindricalGearSetISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _392

        return self.__parent__._cast(
            _392.BevelVirtualCylindricalGearSetISO10300MethodB1
        )

    @property
    def bevel_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_393.BevelVirtualCylindricalGearSetISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _393

        return self.__parent__._cast(
            _393.BevelVirtualCylindricalGearSetISO10300MethodB2
        )

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_395.HypoidVirtualCylindricalGearSetISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _395

        return self.__parent__._cast(
            _395.HypoidVirtualCylindricalGearSetISO10300MethodB1
        )

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_396.HypoidVirtualCylindricalGearSetISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _396

        return self.__parent__._cast(
            _396.HypoidVirtualCylindricalGearSetISO10300MethodB2
        )

    @property
    def klingelnberg_virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_400.KlingelnbergVirtualCylindricalGearSet":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _400

        return self.__parent__._cast(_400.KlingelnbergVirtualCylindricalGearSet)

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_406.VirtualCylindricalGearSetISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _406

        return self.__parent__._cast(_406.VirtualCylindricalGearSetISO10300MethodB1)

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_407.VirtualCylindricalGearSetISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _407

        return self.__parent__._cast(_407.VirtualCylindricalGearSetISO10300MethodB2)

    @property
    def virtual_cylindrical_gear_set(self: "CastSelf") -> "VirtualCylindricalGearSet":
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
class VirtualCylindricalGearSet(_0.APIBase, Generic[T]):
    """VirtualCylindricalGearSet

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def effective_face_width_of_virtual_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveFaceWidthOfVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def face_contact_ratio_transverse_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceContactRatioTransverseForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def face_width_of_virtual_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceWidthOfVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_contact_ratio_normal_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioNormalForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_contact_ratio_for_virtual_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_contact_ratio_transverse_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualContactRatioTransverseForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_pinion(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def virtual_wheel(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def virtual_cylindrical_gears(self: "Self") -> "List[T]":
        """List[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualCylindricalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearSet":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearSet
        """
        return _Cast_VirtualCylindricalGearSet(self)
