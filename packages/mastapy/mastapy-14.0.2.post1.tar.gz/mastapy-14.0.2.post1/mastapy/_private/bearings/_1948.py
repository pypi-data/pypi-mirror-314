"""RollingBearingDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _1949
from mastapy._private.bearings.bearing_designs.rolling import _2221
from mastapy._private.utility.databases import _1886

_ROLLING_BEARING_TYPE = python_net_import("SMT.MastaAPI.Bearings", "RollingBearingType")
_BEARING_CATALOG = python_net_import("SMT.MastaAPI.Bearings", "BearingCatalog")
_HYBRID_STEEL_ALL = python_net_import("SMT.MastaAPI.Bearings", "HybridSteelAll")
_ROLLING_BEARING_DATABASE = python_net_import(
    "SMT.MastaAPI.Bearings", "RollingBearingDatabase"
)
_STRING = python_net_import("System", "String")
_INT_32 = python_net_import("System", "Int32")
_RANGE = python_net_import("SMT.MastaAPI.MathUtility", "Range")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1924, _1940, _1951
    from mastapy._private.math_utility import _1539
    from mastapy._private.utility.databases import _1879

    Self = TypeVar("Self", bound="RollingBearingDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingBearingDatabase._Cast_RollingBearingDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingDatabase:
    """Special nested class for casting RollingBearingDatabase to subclasses."""

    __parent__: "RollingBearingDatabase"

    @property
    def sql_database(self: "CastSelf") -> "_1886.SQLDatabase":
        return self.__parent__._cast(_1886.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1879.Database":
        from mastapy._private.utility.databases import _1879

        return self.__parent__._cast(_1879.Database)

    @property
    def rolling_bearing_database(self: "CastSelf") -> "RollingBearingDatabase":
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
class RollingBearingDatabase(
    _1886.SQLDatabase[_1949.RollingBearingKey, _2221.RollingBearing]
):
    """RollingBearingDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def add_to_database(self: "Self", bearing: "_2221.RollingBearing") -> None:
        """Method does not return.

        Args:
            bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        """
        pythonnet_method_call(
            self.wrapped, "AddToDatabase", bearing.wrapped if bearing else None
        )

    @enforce_parameter_types
    def create_bearing(
        self: "Self", type_: "_1951.RollingBearingType", designation: "str" = "None"
    ) -> "_2221.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            type_ (mastapy.bearings.RollingBearingType)
            designation (str, optional)
        """
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateBearing",
            [_ROLLING_BEARING_TYPE, _STRING],
            type_,
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def create_bearing_with_type_name(
        self: "Self", type_: "str", designation: "str" = "None"
    ) -> "_2221.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            type_ (str)
            designation (str, optional)
        """
        type_ = str(type_)
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateBearing",
            [_STRING, _STRING],
            type_ if type_ else "",
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def create_key(
        self: "Self", type_: "_1951.RollingBearingType", designation: "str" = "None"
    ) -> "_1949.RollingBearingKey":
        """mastapy.bearings.RollingBearingKey

        Args:
            type_ (mastapy.bearings.RollingBearingType)
            designation (str, optional)
        """
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateKey",
            [_ROLLING_BEARING_TYPE, _STRING],
            type_,
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def create_key_with_type_name(
        self: "Self", type_: "str", designation: "str" = "None"
    ) -> "_1949.RollingBearingKey":
        """mastapy.bearings.RollingBearingKey

        Args:
            type_ (str)
            designation (str, optional)
        """
        type_ = str(type_)
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateKey",
            [_STRING, _STRING],
            type_ if type_ else "",
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def remove_from_database(self: "Self", bearing: "_2221.RollingBearing") -> None:
        """Method does not return.

        Args:
            bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveFromDatabase", bearing.wrapped if bearing else None
        )

    @enforce_parameter_types
    def search_for_rolling_bearing_with_catalog(
        self: "Self", catalog: "_1924.BearingCatalog"
    ) -> "List[_2221.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            catalog (mastapy.bearings.BearingCatalog)
        """
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped, "SearchForRollingBearing", [_BEARING_CATALOG], catalog
            )
        )

    @enforce_parameter_types
    def search_for_rolling_bearing_with_name_and_catalog(
        self: "Self", designation: "str", catalog: "_1924.BearingCatalog"
    ) -> "_2221.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "SearchForRollingBearing",
            [_STRING, _BEARING_CATALOG],
            designation if designation else "",
            catalog,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def search_for_rolling_bearing_with_name_catalog_and_type(
        self: "Self",
        designation: "str",
        catalog: "_1924.BearingCatalog",
        type_: "_1951.RollingBearingType",
    ) -> "List[_2221.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
            type_ (mastapy.bearings.RollingBearingType)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "SearchForRollingBearing",
                [_STRING, _BEARING_CATALOG, _ROLLING_BEARING_TYPE],
                designation if designation else "",
                catalog,
                type_,
            )
        )

    @enforce_parameter_types
    def search_for_rolling_bearing(
        self: "Self",
        designation: "str",
        catalog: "_1924.BearingCatalog",
        type_: "_1951.RollingBearingType",
        bore_range: "_1539.Range",
        outer_diameter_range: "_1539.Range",
        width_range: "_1539.Range",
        dynamic_capacity_range: "_1539.Range",
        number_of_rows: "int",
        material_type: "_1940.HybridSteelAll",
    ) -> "List[_2221.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
            type_ (mastapy.bearings.RollingBearingType)
            bore_range (mastapy.math_utility.Range)
            outer_diameter_range (mastapy.math_utility.Range)
            width_range (mastapy.math_utility.Range)
            dynamic_capacity_range (mastapy.math_utility.Range)
            number_of_rows (int)
            material_type (mastapy.bearings.HybridSteelAll)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        number_of_rows = int(number_of_rows)
        material_type = conversion.mp_to_pn_enum(
            material_type, "SMT.MastaAPI.Bearings.HybridSteelAll"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "SearchForRollingBearing",
                [
                    _STRING,
                    _BEARING_CATALOG,
                    _ROLLING_BEARING_TYPE,
                    _RANGE,
                    _RANGE,
                    _RANGE,
                    _RANGE,
                    _INT_32,
                    _HYBRID_STEEL_ALL,
                ],
                designation if designation else "",
                catalog,
                type_,
                bore_range.wrapped if bore_range else None,
                outer_diameter_range.wrapped if outer_diameter_range else None,
                width_range.wrapped if width_range else None,
                dynamic_capacity_range.wrapped if dynamic_capacity_range else None,
                number_of_rows if number_of_rows else 0,
                material_type,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingDatabase":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingDatabase
        """
        return _Cast_RollingBearingDatabase(self)
