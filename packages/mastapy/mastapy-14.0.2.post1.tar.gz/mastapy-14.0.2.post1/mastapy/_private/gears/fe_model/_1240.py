"""GearSetFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1271

_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_GEAR_SET_FE_MODEL = python_net_import("SMT.MastaAPI.Gears.FEModel", "GearSetFEModel")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private import _7733
    from mastapy._private.gears.analysis import _1257, _1266
    from mastapy._private.gears.fe_model import _1237, _1238
    from mastapy._private.gears.fe_model.conical import _1246
    from mastapy._private.gears.fe_model.cylindrical import _1243
    from mastapy._private.nodal_analysis import _58

    Self = TypeVar("Self", bound="GearSetFEModel")
    CastSelf = TypeVar("CastSelf", bound="GearSetFEModel._Cast_GearSetFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetFEModel:
    """Special nested class for casting GearSetFEModel to subclasses."""

    __parent__: "GearSetFEModel"

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1271.GearSetImplementationDetail":
        return self.__parent__._cast(_1271.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1266.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1257.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1257

        return self.__parent__._cast(_1257.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1243.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1243

        return self.__parent__._cast(_1243.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1246.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1246

        return self.__parent__._cast(_1246.ConicalSetFEModel)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "GearSetFEModel":
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
class GearSetFEModel(_1271.GearSetImplementationDetail):
    """GearSetFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def element_order(self: "Self") -> "_58.ElementOrder":
        """mastapy.nodal_analysis.ElementOrder"""
        temp = pythonnet_property_get(self.wrapped, "ElementOrder")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._58", "ElementOrder"
        )(value)

    @element_order.setter
    @enforce_parameter_types
    def element_order(self: "Self", value: "_58.ElementOrder") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )
        pythonnet_property_set(self.wrapped, "ElementOrder", value)

    @property
    def number_of_coupled_teeth_either_side(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCoupledTeethEitherSide")

        if temp is None:
            return 0

        return temp

    @number_of_coupled_teeth_either_side.setter
    @enforce_parameter_types
    def number_of_coupled_teeth_either_side(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCoupledTeethEitherSide",
            int(value) if value is not None else 0,
        )

    @property
    def use_out_of_core_solver(self: "Self") -> "Optional[bool]":
        """Optional[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseOutOfCoreSolver")

        if temp is None:
            return None

        return temp

    @use_out_of_core_solver.setter
    @enforce_parameter_types
    def use_out_of_core_solver(self: "Self", value: "Optional[bool]") -> None:
        pythonnet_property_set(self.wrapped, "UseOutOfCoreSolver", value)

    @property
    def gear_fe_models(self: "Self") -> "List[_1237.GearFEModel]":
        """List[mastapy.gears.fe_model.GearFEModel]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearFEModels")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mesh_fe_models(self: "Self") -> "List[_1238.GearMeshFEModel]":
        """List[mastapy.gears.fe_model.GearMeshFEModel]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshFEModels")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def is_ready_for_altca(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsReadyForALTCA")

        if temp is None:
            return False

        return temp

    def generate_stiffness_from_fe(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateStiffnessFromFE")

    def generate_stress_influence_coefficients_from_fe(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateStressInfluenceCoefficientsFromFE")

    def calculate_stiffness_from_fe(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateStiffnessFromFE")

    @enforce_parameter_types
    def calculate_stiffness_from_fe_with_progress(
        self: "Self", progress: "_7733.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "CalculateStiffnessFromFE",
            [_TASK_PROGRESS],
            progress.wrapped if progress else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetFEModel":
        """Cast to another type.

        Returns:
            _Cast_GearSetFEModel
        """
        return _Cast_GearSetFEModel(self)
