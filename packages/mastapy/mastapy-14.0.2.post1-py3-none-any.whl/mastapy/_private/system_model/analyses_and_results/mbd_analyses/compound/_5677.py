"""BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5674,
)

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
        "BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5522
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5667,
        _5679,
        _5688,
        _5695,
        _5721,
        _5742,
        _5744,
    )

    Self = TypeVar(
        "Self", bound="BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis._Cast_BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis"

    @property
    def bevel_differential_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5674.BevelDifferentialGearCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5674.BevelDifferentialGearCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5679.BevelGearCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5679,
        )

        return self.__parent__._cast(_5679.BevelGearCompoundMultibodyDynamicsAnalysis)

    @property
    def agma_gleason_conical_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5667.AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5667,
        )

        return self.__parent__._cast(
            _5667.AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5695.ConicalGearCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5695,
        )

        return self.__parent__._cast(_5695.ConicalGearCompoundMultibodyDynamicsAnalysis)

    @property
    def gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5721.GearCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5721,
        )

        return self.__parent__._cast(_5721.GearCompoundMultibodyDynamicsAnalysis)

    @property
    def mountable_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5742.MountableComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5742,
        )

        return self.__parent__._cast(
            _5742.MountableComponentCompoundMultibodyDynamicsAnalysis
        )

    @property
    def component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5688,
        )

        return self.__parent__._cast(_5688.ComponentCompoundMultibodyDynamicsAnalysis)

    @property
    def part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5744.PartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5744,
        )

        return self.__parent__._cast(_5744.PartCompoundMultibodyDynamicsAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartCompoundAnalysis)

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
    def bevel_differential_planet_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis":
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
class BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis(
    _5674.BevelDifferentialGearCompoundMultibodyDynamicsAnalysis
):
    """BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5522.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5522.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis(self)
