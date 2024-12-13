"""GearImplementationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1258

_GEAR_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1255
    from mastapy._private.gears.fe_model import _1237
    from mastapy._private.gears.fe_model.conical import _1244
    from mastapy._private.gears.fe_model.cylindrical import _1241
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1134,
        _1135,
        _1138,
    )
    from mastapy._private.gears.gear_designs.face import _1019
    from mastapy._private.gears.manufacturing.bevel import (
        _801,
        _802,
        _803,
        _813,
        _814,
        _819,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _637
    from mastapy._private.utility.scripting import _1794

    Self = TypeVar("Self", bound="GearImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="GearImplementationDetail._Cast_GearImplementationDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearImplementationDetail:
    """Special nested class for casting GearImplementationDetail to subclasses."""

    __parent__: "GearImplementationDetail"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1258.GearDesignAnalysis":
        return self.__parent__._cast(_1258.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1255.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1255

        return self.__parent__._cast(_1255.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_637.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _637

        return self.__parent__._cast(_637.CylindricalGearManufacturingConfig)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_801.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _801

        return self.__parent__._cast(_801.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_802.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _802

        return self.__parent__._cast(_802.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_803.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _803

        return self.__parent__._cast(_803.ConicalGearMicroGeometryConfigBase)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_813.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _813

        return self.__parent__._cast(_813.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_814.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _814

        return self.__parent__._cast(_814.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_819.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _819

        return self.__parent__._cast(_819.ConicalWheelManufacturingConfig)

    @property
    def face_gear_micro_geometry(self: "CastSelf") -> "_1019.FaceGearMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1019

        return self.__parent__._cast(_1019.FaceGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "_1134.CylindricalGearMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1134

        return self.__parent__._cast(_1134.CylindricalGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1135.CylindricalGearMicroGeometryBase":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1135

        return self.__parent__._cast(_1135.CylindricalGearMicroGeometryBase)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearMicroGeometryPerTooth":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1138

        return self.__parent__._cast(_1138.CylindricalGearMicroGeometryPerTooth)

    @property
    def gear_fe_model(self: "CastSelf") -> "_1237.GearFEModel":
        from mastapy._private.gears.fe_model import _1237

        return self.__parent__._cast(_1237.GearFEModel)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1241.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1241

        return self.__parent__._cast(_1241.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1244.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1244

        return self.__parent__._cast(_1244.ConicalGearFEModel)

    @property
    def gear_implementation_detail(self: "CastSelf") -> "GearImplementationDetail":
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
class GearImplementationDetail(_1258.GearDesignAnalysis):
    """GearImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_IMPLEMENTATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def user_specified_data(self: "Self") -> "_1794.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearImplementationDetail
        """
        return _Cast_GearImplementationDetail(self)
