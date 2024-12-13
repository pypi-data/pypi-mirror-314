"""PartCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7720

_PART_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "PartCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7247,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7297,
        _7298,
        _7299,
        _7301,
        _7303,
        _7304,
        _7305,
        _7307,
        _7308,
        _7310,
        _7311,
        _7312,
        _7313,
        _7315,
        _7316,
        _7317,
        _7318,
        _7320,
        _7322,
        _7323,
        _7325,
        _7326,
        _7328,
        _7329,
        _7331,
        _7333,
        _7334,
        _7336,
        _7338,
        _7339,
        _7340,
        _7342,
        _7344,
        _7346,
        _7347,
        _7348,
        _7349,
        _7350,
        _7352,
        _7353,
        _7354,
        _7355,
        _7357,
        _7358,
        _7359,
        _7361,
        _7363,
        _7365,
        _7366,
        _7368,
        _7369,
        _7371,
        _7372,
        _7373,
        _7374,
        _7375,
        _7376,
        _7377,
        _7379,
        _7381,
        _7383,
        _7384,
        _7385,
        _7386,
        _7387,
        _7388,
        _7390,
        _7391,
        _7393,
        _7394,
        _7395,
        _7397,
        _7398,
        _7400,
        _7401,
        _7403,
        _7404,
        _7406,
        _7407,
        _7409,
        _7410,
        _7411,
        _7412,
        _7413,
        _7414,
        _7415,
        _7416,
        _7418,
        _7419,
        _7420,
        _7421,
        _7422,
        _7424,
        _7425,
        _7427,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

    Self = TypeVar(
        "Self", bound="PartCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_PartCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting PartCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "PartCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7720.PartCompoundAnalysis":
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
    def abstract_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7297.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7297,
        )

        return self.__parent__._cast(
            _7297.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7298.AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7298,
        )

        return self.__parent__._cast(
            _7298.AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_or_housing_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7299.AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7299,
        )

        return self.__parent__._cast(
            _7299.AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7301.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7301,
        )

        return self.__parent__._cast(
            _7301.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7303.AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7303,
        )

        return self.__parent__._cast(
            _7303.AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7304.AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7304,
        )

        return self.__parent__._cast(
            _7304.AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bearing_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7305.BearingCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7305,
        )

        return self.__parent__._cast(
            _7305.BearingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_drive_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7307.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7307,
        )

        return self.__parent__._cast(
            _7307.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7308.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7308,
        )

        return self.__parent__._cast(
            _7308.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7310.BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7310,
        )

        return self.__parent__._cast(
            _7310.BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7311.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7311,
        )

        return self.__parent__._cast(
            _7311.BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7312.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7312,
        )

        return self.__parent__._cast(
            _7312.BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7313.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7313,
        )

        return self.__parent__._cast(
            _7313.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7315.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7315,
        )

        return self.__parent__._cast(
            _7315.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolt_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7316.BoltCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7316,
        )

        return self.__parent__._cast(
            _7316.BoltCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolted_joint_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7317.BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7317,
        )

        return self.__parent__._cast(
            _7317.BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7318.ClutchCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7318,
        )

        return self.__parent__._cast(
            _7318.ClutchCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7320.ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7320,
        )

        return self.__parent__._cast(
            _7320.ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7322.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7322,
        )

        return self.__parent__._cast(
            _7322.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7323.ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7323,
        )

        return self.__parent__._cast(
            _7323.ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7325.ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7325,
        )

        return self.__parent__._cast(
            _7325.ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7326.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7326,
        )

        return self.__parent__._cast(
            _7326.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7328.ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7328,
        )

        return self.__parent__._cast(
            _7328.ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7329.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7329,
        )

        return self.__parent__._cast(
            _7329.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7331.ConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7331,
        )

        return self.__parent__._cast(
            _7331.ConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connector_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7333.ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7333,
        )

        return self.__parent__._cast(
            _7333.ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7334.CouplingCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7334,
        )

        return self.__parent__._cast(
            _7334.CouplingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7336.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7336,
        )

        return self.__parent__._cast(
            _7336.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7338.CVTCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7338,
        )

        return self.__parent__._cast(
            _7338.CVTCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_pulley_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7339.CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7339,
        )

        return self.__parent__._cast(
            _7339.CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7340.CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7340,
        )

        return self.__parent__._cast(
            _7340.CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7342.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7342,
        )

        return self.__parent__._cast(
            _7342.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7344.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7344,
        )

        return self.__parent__._cast(
            _7344.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7346.CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7346,
        )

        return self.__parent__._cast(
            _7346.CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7347.CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7347,
        )

        return self.__parent__._cast(
            _7347.CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def datum_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7348.DatumCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7348,
        )

        return self.__parent__._cast(
            _7348.DatumCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def external_cad_model_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7349.ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7349,
        )

        return self.__parent__._cast(
            _7349.ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7350.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7350,
        )

        return self.__parent__._cast(
            _7350.FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7352.FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7352,
        )

        return self.__parent__._cast(
            _7352.FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def fe_part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7353.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7353,
        )

        return self.__parent__._cast(
            _7353.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def flexible_pin_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7354.FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7354,
        )

        return self.__parent__._cast(
            _7354.FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7355.GearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7355,
        )

        return self.__parent__._cast(
            _7355.GearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7357.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7357,
        )

        return self.__parent__._cast(
            _7357.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def guide_dxf_model_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7358.GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7358,
        )

        return self.__parent__._cast(
            _7358.GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7359.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7359,
        )

        return self.__parent__._cast(
            _7359.HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7361.HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7361,
        )

        return self.__parent__._cast(
            _7361.HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7363.KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7363,
        )

        return self.__parent__._cast(
            _7363.KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7365.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7365,
        )

        return self.__parent__._cast(
            _7365.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7366.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7366,
        )

        return self.__parent__._cast(
            _7366.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7368.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7368,
        )

        return self.__parent__._cast(
            _7368.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7369.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7369,
        )

        return self.__parent__._cast(
            _7369.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7371.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7371,
        )

        return self.__parent__._cast(
            _7371.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mass_disc_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7372.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7372,
        )

        return self.__parent__._cast(
            _7372.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7373.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7373,
        )

        return self.__parent__._cast(
            _7373.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_array_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7374.MicrophoneArrayCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7374,
        )

        return self.__parent__._cast(
            _7374.MicrophoneArrayCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7375.MicrophoneCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7375,
        )

        return self.__parent__._cast(
            _7375.MicrophoneCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7376.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7376,
        )

        return self.__parent__._cast(
            _7376.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def oil_seal_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7377.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7377,
        )

        return self.__parent__._cast(
            _7377.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7379.PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7379,
        )

        return self.__parent__._cast(
            _7379.PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7381.PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7381,
        )

        return self.__parent__._cast(
            _7381.PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7383.PlanetaryGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7383,
        )

        return self.__parent__._cast(
            _7383.PlanetaryGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planet_carrier_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7384.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7384,
        )

        return self.__parent__._cast(
            _7384.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7385.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7385,
        )

        return self.__parent__._cast(
            _7385.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7386.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7386,
        )

        return self.__parent__._cast(
            _7386.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def pulley_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7387.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7387,
        )

        return self.__parent__._cast(
            _7387.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7388.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7388,
        )

        return self.__parent__._cast(
            _7388.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7390.RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7390,
        )

        return self.__parent__._cast(
            _7390.RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7391.RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7391,
        )

        return self.__parent__._cast(
            _7391.RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def root_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7393.RootAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7393,
        )

        return self.__parent__._cast(
            _7393.RootAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7394.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7394,
        )

        return self.__parent__._cast(
            _7394.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_hub_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7395.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7395,
        )

        return self.__parent__._cast(
            _7395.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def specialised_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7397.SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7397,
        )

        return self.__parent__._cast(
            _7397.SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7398.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7398,
        )

        return self.__parent__._cast(
            _7398.SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7400.SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7400,
        )

        return self.__parent__._cast(
            _7400.SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7401.SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7401,
        )

        return self.__parent__._cast(
            _7401.SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7403.SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7403,
        )

        return self.__parent__._cast(
            _7403.SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7404.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7404,
        )

        return self.__parent__._cast(
            _7404.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7406.StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7406,
        )

        return self.__parent__._cast(
            _7406.StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7407.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7407,
        )

        return self.__parent__._cast(
            _7407.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7409.StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7409,
        )

        return self.__parent__._cast(
            _7409.StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7410.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7410,
        )

        return self.__parent__._cast(
            _7410.StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7411.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7411,
        )

        return self.__parent__._cast(
            _7411.StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7412.SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7412,
        )

        return self.__parent__._cast(
            _7412.SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7413.SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7413,
        )

        return self.__parent__._cast(
            _7413.SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7414.SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7414,
        )

        return self.__parent__._cast(
            _7414.SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_sleeve_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7415.SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7415,
        )

        return self.__parent__._cast(
            _7415.SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7416.TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7416,
        )

        return self.__parent__._cast(
            _7416.TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_pump_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7418.TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7418,
        )

        return self.__parent__._cast(
            _7418.TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_turbine_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7419.TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7419,
        )

        return self.__parent__._cast(
            _7419.TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7420.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7420,
        )

        return self.__parent__._cast(
            _7420.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7421.VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7421,
        )

        return self.__parent__._cast(
            _7421.VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7422.WormGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7422,
        )

        return self.__parent__._cast(
            _7422.WormGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7424.WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7424,
        )

        return self.__parent__._cast(
            _7424.WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7425.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7425,
        )

        return self.__parent__._cast(
            _7425.ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_set_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7427.ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7427,
        )

        return self.__parent__._cast(
            _7427.ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "PartCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class PartCompoundAdvancedTimeSteppingAnalysisForModulation(_7720.PartCompoundAnalysis):
    """PartCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PART_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7247.PartAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.PartAdvancedTimeSteppingAnalysisForModulation]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7247.PartAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.PartAdvancedTimeSteppingAnalysisForModulation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_PartCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_PartCompoundAdvancedTimeSteppingAnalysisForModulation(self)
