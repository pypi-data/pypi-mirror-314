"""HarmonicLoadDataFluxImport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7032, _7051

_HARMONIC_LOAD_DATA_FLUX_IMPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataFluxImport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7054,
        _7055,
        _7063,
    )

    Self = TypeVar("Self", bound="HarmonicLoadDataFluxImport")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicLoadDataFluxImport._Cast_HarmonicLoadDataFluxImport"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataFluxImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataFluxImport:
    """Special nested class for casting HarmonicLoadDataFluxImport to subclasses."""

    __parent__: "HarmonicLoadDataFluxImport"

    @property
    def harmonic_load_data_csv_import(
        self: "CastSelf",
    ) -> "_7051.HarmonicLoadDataCSVImport":
        return self.__parent__._cast(_7051.HarmonicLoadDataCSVImport)

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "_7055.HarmonicLoadDataImportFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7055,
        )

        return self.__parent__._cast(_7055.HarmonicLoadDataImportFromMotorPackages)

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "_7054.HarmonicLoadDataImportBase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7054,
        )

        return self.__parent__._cast(_7054.HarmonicLoadDataImportBase)

    @property
    def harmonic_load_data_flux_import(
        self: "CastSelf",
    ) -> "HarmonicLoadDataFluxImport":
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
class HarmonicLoadDataFluxImport(
    _7051.HarmonicLoadDataCSVImport[_7032.ElectricMachineHarmonicLoadFluxImportOptions]
):
    """HarmonicLoadDataFluxImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_FLUX_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def diameter_of_node_ring_from_flux_file(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterOfNodeRingFromFluxFile")

        if temp is None:
            return 0.0

        return temp

    @property
    def inner_diameter_reference(self: "Self") -> "_7063.InnerDiameterReference":
        """mastapy.system_model.analyses_and_results.static_loads.InnerDiameterReference"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameterReference")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.InnerDiameterReference",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7063",
            "InnerDiameterReference",
        )(value)

    @inner_diameter_reference.setter
    @enforce_parameter_types
    def inner_diameter_reference(
        self: "Self", value: "_7063.InnerDiameterReference"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.InnerDiameterReference",
        )
        pythonnet_property_set(self.wrapped, "InnerDiameterReference", value)

    def select_flux_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectFluxFile")

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataFluxImport":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataFluxImport
        """
        return _Cast_HarmonicLoadDataFluxImport(self)
