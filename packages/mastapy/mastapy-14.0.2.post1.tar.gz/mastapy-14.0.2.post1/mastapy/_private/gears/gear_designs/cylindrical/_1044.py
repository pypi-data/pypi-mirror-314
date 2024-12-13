"""CylindricalGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _973

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYLINDRICAL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _345
    from mastapy._private.gears.gear_designs import _974
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1027,
        _1032,
        _1035,
        _1036,
        _1042,
        _1049,
        _1050,
        _1052,
        _1054,
        _1060,
        _1074,
        _1078,
        _1087,
        _1112,
        _1114,
        _1118,
        _1119,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1173,
        _1178,
        _1179,
        _1180,
        _1184,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1135
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1123,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _637
    from mastapy._private.gears.materials import _610
    from mastapy._private.gears.rating.cylindrical import _467
    from mastapy._private.geometry.two_d import _324

    Self = TypeVar("Self", bound="CylindricalGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearDesign._Cast_CylindricalGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesign:
    """Special nested class for casting CylindricalGearDesign to subclasses."""

    __parent__: "CylindricalGearDesign"

    @property
    def gear_design(self: "CastSelf") -> "_973.GearDesign":
        return self.__parent__._cast(_973.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_974.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _974

        return self.__parent__._cast(_974.GearDesignComponent)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1074.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1074

        return self.__parent__._cast(_1074.CylindricalPlanetGearDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "CylindricalGearDesign":
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
class CylindricalGearDesign(_973.GearDesign):
    """CylindricalGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def absolute_rim_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteRimDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return temp

    @property
    def aspect_ratio_face_width_reference_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AspectRatioFaceWidthReferenceDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    def effective_web_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveWebThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def factor_for_the_increase_of_the_yield_point_under_compression(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FactorForTheIncreaseOfTheYieldPointUnderCompression"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @factor_for_the_increase_of_the_yield_point_under_compression.setter
    @enforce_parameter_types
    def factor_for_the_increase_of_the_yield_point_under_compression(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "FactorForTheIncreaseOfTheYieldPointUnderCompression", value
        )

    @property
    def flank_heat_transfer_coefficient(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FlankHeatTransferCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flank_heat_transfer_coefficient.setter
    @enforce_parameter_types
    def flank_heat_transfer_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FlankHeatTransferCoefficient", value)

    @property
    def gear_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def gear_hand(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearHand")

        if temp is None:
            return ""

        return temp

    @property
    def gear_tooth_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearToothDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def hand(self: "Self") -> "_345.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._345", "Hand")(
            value
        )

    @hand.setter
    @enforce_parameter_types
    def hand(self: "Self", value: "_345.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    def helix_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def helix_angle_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleAtTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def initial_clocking_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialClockingAngle")

        if temp is None:
            return 0.0

        return temp

    @initial_clocking_angle.setter
    @enforce_parameter_types
    def initial_clocking_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InitialClockingAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def internal_external(self: "Self") -> "_324.InternalExternalType":
        """mastapy.geometry.two_d.InternalExternalType"""
        temp = pythonnet_property_get(self.wrapped, "InternalExternal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.geometry.two_d._324", "InternalExternalType"
        )(value)

    @internal_external.setter
    @enforce_parameter_types
    def internal_external(self: "Self", value: "_324.InternalExternalType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )
        pythonnet_property_set(self.wrapped, "InternalExternal", value)

    @property
    def is_asymmetric(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsAsymmetric")

        if temp is None:
            return False

        return temp

    @property
    def lead(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Lead")

        if temp is None:
            return 0.0

        return temp

    @property
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    def material_agma(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MaterialAGMA", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @material_agma.setter
    @enforce_parameter_types
    def material_agma(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "MaterialAGMA",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def material_iso(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MaterialISO", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @material_iso.setter
    @enforce_parameter_types
    def material_iso(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "MaterialISO",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def material_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialName")

        if temp is None:
            return ""

        return temp

    @property
    def mean_generating_circle_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanGeneratingCircleDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_normal_thickness_at_half_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanNormalThicknessAtHalfDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_rim_thickness_normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRimThicknessNormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_space_width_at_root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalSpaceWidthAtRootFormDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_space_width_at_root_form_diameter_over_normal_module(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalSpaceWidthAtRootFormDiameterOverNormalModule"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_lower_backlash_allowance(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalThicknessAtTipFormDiameterAtLowerBacklashAllowance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_lower_backlash_allowance_over_normal_module(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "NormalThicknessAtTipFormDiameterAtLowerBacklashAllowanceOverNormalModule",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_upper_backlash_allowance(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalThicknessAtTipFormDiameterAtUpperBacklashAllowance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_tooth_thickness_at_the_base_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalToothThicknessAtTheBaseCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_teeth_unsigned(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethUnsigned")

        if temp is None:
            return 0.0

        return temp

    @number_of_teeth_unsigned.setter
    @enforce_parameter_types
    def number_of_teeth_unsigned(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethUnsigned",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_teeth_with_centre_distance_adjustment(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTeethWithCentreDistanceAdjustment"
        )

        if temp is None:
            return 0

        return temp

    @number_of_teeth_with_centre_distance_adjustment.setter
    @enforce_parameter_types
    def number_of_teeth_with_centre_distance_adjustment(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethWithCentreDistanceAdjustment",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_teeth_maintaining_ratio_calculating_normal_module(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTeethMaintainingRatioCalculatingNormalModule"
        )

        if temp is None:
            return 0

        return temp

    @number_of_teeth_maintaining_ratio_calculating_normal_module.setter
    @enforce_parameter_types
    def number_of_teeth_maintaining_ratio_calculating_normal_module(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethMaintainingRatioCalculatingNormalModule",
            int(value) if value is not None else 0,
        )

    @property
    def number_of_teeth_with_normal_module_adjustment(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTeethWithNormalModuleAdjustment"
        )

        if temp is None:
            return 0

        return temp

    @number_of_teeth_with_normal_module_adjustment.setter
    @enforce_parameter_types
    def number_of_teeth_with_normal_module_adjustment(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethWithNormalModuleAdjustment",
            int(value) if value is not None else 0,
        )

    @property
    def permissible_linear_wear(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PermissibleLinearWear")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_linear_wear.setter
    @enforce_parameter_types
    def permissible_linear_wear(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PermissibleLinearWear", value)

    @property
    def reference_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def rim_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RimDiameter")

        if temp is None:
            return 0.0

        return temp

    @rim_diameter.setter
    @enforce_parameter_types
    def rim_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RimDiameter", float(value) if value is not None else 0.0
        )

    @property
    def rim_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RimThickness")

        if temp is None:
            return 0.0

        return temp

    @rim_thickness.setter
    @enforce_parameter_types
    def rim_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RimThickness", float(value) if value is not None else 0.0
        )

    @property
    def rim_thickness_normal_module_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RimThicknessNormalModuleRatio")

        if temp is None:
            return 0.0

        return temp

    @rim_thickness_normal_module_ratio.setter
    @enforce_parameter_types
    def rim_thickness_normal_module_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RimThicknessNormalModuleRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def root_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_diameter.setter
    @enforce_parameter_types
    def root_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootDiameter", value)

    @property
    def root_diameter_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameterLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def root_heat_transfer_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootHeatTransferCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_heat_transfer_coefficient.setter
    @enforce_parameter_types
    def root_heat_transfer_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootHeatTransferCoefficient", value)

    @property
    def rotation_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_tip_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SignedTipDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @signed_tip_diameter.setter
    @enforce_parameter_types
    def signed_tip_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SignedTipDiameter", value)

    @property
    def specified_web_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedWebThickness")

        if temp is None:
            return 0.0

        return temp

    @specified_web_thickness.setter
    @enforce_parameter_types
    def specified_web_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedWebThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    def thermal_contact_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThermalContactCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thermal_contact_coefficient.setter
    @enforce_parameter_types
    def thermal_contact_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThermalContactCoefficient", value)

    @property
    def tip_alteration_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TipAlterationCoefficient")

        if temp is None:
            return 0.0

        return temp

    @tip_alteration_coefficient.setter
    @enforce_parameter_types
    def tip_alteration_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TipAlterationCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def tip_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tip_diameter.setter
    @enforce_parameter_types
    def tip_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TipDiameter", value)

    @property
    def tip_diameter_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameterLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_thickness_at_lower_backlash_allowance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipThicknessAtLowerBacklashAllowance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_thickness_at_lower_backlash_allowance_over_normal_module(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipThicknessAtLowerBacklashAllowanceOverNormalModule"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tip_thickness_at_upper_backlash_allowance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipThicknessAtUpperBacklashAllowance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_tooth_thickness_at_the_base_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseToothThicknessAtTheBaseCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def use_default_design_material(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultDesignMaterial")

        if temp is None:
            return False

        return temp

    @use_default_design_material.setter
    @enforce_parameter_types
    def use_default_design_material(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultDesignMaterial",
            bool(value) if value is not None else False,
        )

    @property
    def web_centre_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WebCentreOffset")

        if temp is None:
            return 0.0

        return temp

    @web_centre_offset.setter
    @enforce_parameter_types
    def web_centre_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WebCentreOffset", float(value) if value is not None else 0.0
        )

    @property
    def web_status(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WebStatus")

        if temp is None:
            return ""

        return temp

    @property
    def agma_accuracy_grade(self: "Self") -> "_1173.AGMA20151AccuracyGrades":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.AGMA20151AccuracyGrades

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMAAccuracyGrade")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def accuracy_grades_specified_accuracy(
        self: "Self",
    ) -> "_1178.CylindricalAccuracyGrades":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.CylindricalAccuracyGrades

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccuracyGradesSpecifiedAccuracy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def case_hardening_properties(self: "Self") -> "_1027.CaseHardeningProperties":
        """mastapy.gears.gear_designs.cylindrical.CaseHardeningProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CaseHardeningProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_cutting_options(
        self: "Self",
    ) -> "_1042.CylindricalGearCuttingOptions":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearCuttingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearCuttingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_manufacturing_configuration(
        self: "Self",
    ) -> "_637.CylindricalGearManufacturingConfig":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearManufacturingConfiguration"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_micro_geometry(
        self: "Self",
    ) -> "_1135.CylindricalGearMicroGeometryBase":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMicroGeometryBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "Self",
    ) -> "_1054.CylindricalGearMicroGeometrySettingsItem":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMicroGeometrySettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_set(self: "Self") -> "_1060.CylindricalGearSetDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def customer_102_data_sheet_change_log(
        self: "Self",
    ) -> "_1032.Customer102DataSheetChangeLog":
        """mastapy.gears.gear_designs.cylindrical.Customer102DataSheetChangeLog

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Customer102DataSheetChangeLog")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def customer_102_data_sheet_notes(
        self: "Self",
    ) -> "_1035.Customer102DataSheetNotes":
        """mastapy.gears.gear_designs.cylindrical.Customer102DataSheetNotes

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Customer102DataSheetNotes")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def customer_102_data_sheet_tolerance_settings(
        self: "Self",
    ) -> "_1036.Customer102DataSheetTolerances":
        """mastapy.gears.gear_designs.cylindrical.Customer102DataSheetTolerances

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "Customer102DataSheetToleranceSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def finish_stock_specification(self: "Self") -> "_1123.FinishStockSpecification":
        """mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishStockSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def finished_tooth_thickness_specification(
        self: "Self",
    ) -> "_1078.FinishToothThicknessDesignSpecification":
        """mastapy.gears.gear_designs.cylindrical.FinishToothThicknessDesignSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FinishedToothThicknessSpecification"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1179.CylindricalGearAccuracyTolerances":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.CylindricalGearAccuracyTolerances

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAccuracyTolerances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso6336_geometry(self: "Self") -> "_1087.ISO6336GeometryBase":
        """mastapy.gears.gear_designs.cylindrical.ISO6336GeometryBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336Geometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso_accuracy_grade(self: "Self") -> "_1184.ISO1328AccuracyGrades":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.ISO1328AccuracyGrades

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOAccuracyGrade")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_flank(self: "Self") -> "_1049.CylindricalGearFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def material(self: "Self") -> "_610.GearMaterial":
        """mastapy.gears.materials.GearMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Material")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def micro_geometry_settings(
        self: "Self",
    ) -> "_1052.CylindricalGearMicroGeometrySettings":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometrySettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating_settings(
        self: "Self",
    ) -> "_467.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank(self: "Self") -> "_1049.CylindricalGearFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rough_tooth_thickness_specification(
        self: "Self",
    ) -> "_1119.ToothThicknessSpecification":
        """mastapy.gears.gear_designs.cylindrical.ToothThicknessSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughToothThicknessSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def surface_roughness(self: "Self") -> "_1112.SurfaceRoughness":
        """mastapy.gears.gear_designs.cylindrical.SurfaceRoughness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceRoughness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_of_gear_fits(self: "Self") -> "_1180.DIN3967SystemOfGearFits":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.DIN3967SystemOfGearFits

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemOfGearFits")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tff_analysis_settings(
        self: "Self",
    ) -> "_1118.ToothFlankFractureAnalysisSettings":
        """mastapy.gears.gear_designs.cylindrical.ToothFlankFractureAnalysisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TFFAnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tiff_analysis_settings(self: "Self") -> "_1114.TiffAnalysisSettings":
        """mastapy.gears.gear_designs.cylindrical.TiffAnalysisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFAnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_meshes(self: "Self") -> "List[_1050.CylindricalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def flanks(self: "Self") -> "List[_1049.CylindricalGearFlankDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearFlankDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def both_flanks(self: "Self") -> "_1049.CylindricalGearFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def manufacturing_configurations(
        self: "Self",
    ) -> "List[_637.CylindricalGearManufacturingConfig]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalGearManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def micro_geometries(
        self: "Self",
    ) -> "List[_1135.CylindricalGearMicroGeometryBase]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMicroGeometryBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesign
        """
        return _Cast_CylindricalGearDesign(self)
