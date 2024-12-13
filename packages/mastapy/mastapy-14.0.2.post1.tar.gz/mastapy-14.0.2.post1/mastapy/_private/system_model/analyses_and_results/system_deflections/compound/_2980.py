"""CouplingConnectionCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3008,
)

_COUPLING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "CouplingConnectionCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7713,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2818,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2964,
        _2969,
        _2977,
        _3026,
        _3049,
        _3064,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundSystemDeflection._Cast_CouplingConnectionCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundSystemDeflection:
    """Special nested class for casting CouplingConnectionCompoundSystemDeflection to subclasses."""

    __parent__: "CouplingConnectionCompoundSystemDeflection"

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3008.InterMountableComponentConnectionCompoundSystemDeflection":
        return self.__parent__._cast(
            _3008.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2977.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2977,
        )

        return self.__parent__._cast(_2977.ConnectionCompoundSystemDeflection)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7713.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7717.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def clutch_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2964.ClutchConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2964,
        )

        return self.__parent__._cast(_2964.ClutchConnectionCompoundSystemDeflection)

    @property
    def concept_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConceptCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2969,
        )

        return self.__parent__._cast(
            _2969.ConceptCouplingConnectionCompoundSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3026.PartToPartShearCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3026,
        )

        return self.__parent__._cast(
            _3026.PartToPartShearCouplingConnectionCompoundSystemDeflection
        )

    @property
    def spring_damper_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3049.SpringDamperConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3049,
        )

        return self.__parent__._cast(
            _3049.SpringDamperConnectionCompoundSystemDeflection
        )

    @property
    def torque_converter_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3064.TorqueConverterConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3064,
        )

        return self.__parent__._cast(
            _3064.TorqueConverterConnectionCompoundSystemDeflection
        )

    @property
    def coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundSystemDeflection":
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
class CouplingConnectionCompoundSystemDeflection(
    _3008.InterMountableComponentConnectionCompoundSystemDeflection
):
    """CouplingConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2818.CouplingConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2818.CouplingConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundSystemDeflection
        """
        return _Cast_CouplingConnectionCompoundSystemDeflection(self)
