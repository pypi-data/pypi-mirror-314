"""PartCompoundModalAnalysis"""

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

_PART_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "PartCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4781
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4847,
        _4848,
        _4849,
        _4851,
        _4853,
        _4854,
        _4855,
        _4857,
        _4858,
        _4860,
        _4861,
        _4862,
        _4863,
        _4865,
        _4866,
        _4867,
        _4868,
        _4870,
        _4872,
        _4873,
        _4875,
        _4876,
        _4878,
        _4879,
        _4881,
        _4883,
        _4884,
        _4886,
        _4888,
        _4889,
        _4890,
        _4892,
        _4894,
        _4896,
        _4897,
        _4898,
        _4899,
        _4900,
        _4902,
        _4903,
        _4904,
        _4905,
        _4907,
        _4908,
        _4909,
        _4911,
        _4913,
        _4915,
        _4916,
        _4918,
        _4919,
        _4921,
        _4922,
        _4923,
        _4924,
        _4925,
        _4926,
        _4927,
        _4929,
        _4931,
        _4933,
        _4934,
        _4935,
        _4936,
        _4937,
        _4938,
        _4940,
        _4941,
        _4943,
        _4944,
        _4945,
        _4947,
        _4948,
        _4950,
        _4951,
        _4953,
        _4954,
        _4956,
        _4957,
        _4959,
        _4960,
        _4961,
        _4962,
        _4963,
        _4964,
        _4965,
        _4966,
        _4968,
        _4969,
        _4970,
        _4971,
        _4972,
        _4974,
        _4975,
        _4977,
    )

    Self = TypeVar("Self", bound="PartCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="PartCompoundModalAnalysis._Cast_PartCompoundModalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundModalAnalysis:
    """Special nested class for casting PartCompoundModalAnalysis to subclasses."""

    __parent__: "PartCompoundModalAnalysis"

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
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4847.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4847,
        )

        return self.__parent__._cast(_4847.AbstractAssemblyCompoundModalAnalysis)

    @property
    def abstract_shaft_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4848.AbstractShaftCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4848,
        )

        return self.__parent__._cast(_4848.AbstractShaftCompoundModalAnalysis)

    @property
    def abstract_shaft_or_housing_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4849.AbstractShaftOrHousingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4849,
        )

        return self.__parent__._cast(_4849.AbstractShaftOrHousingCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4851.AGMAGleasonConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4851,
        )

        return self.__parent__._cast(_4851.AGMAGleasonConicalGearCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4853.AGMAGleasonConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4853,
        )

        return self.__parent__._cast(
            _4853.AGMAGleasonConicalGearSetCompoundModalAnalysis
        )

    @property
    def assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4854.AssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4854,
        )

        return self.__parent__._cast(_4854.AssemblyCompoundModalAnalysis)

    @property
    def bearing_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4855.BearingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4855,
        )

        return self.__parent__._cast(_4855.BearingCompoundModalAnalysis)

    @property
    def belt_drive_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4857.BeltDriveCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4857,
        )

        return self.__parent__._cast(_4857.BeltDriveCompoundModalAnalysis)

    @property
    def bevel_differential_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4858.BevelDifferentialGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4858,
        )

        return self.__parent__._cast(_4858.BevelDifferentialGearCompoundModalAnalysis)

    @property
    def bevel_differential_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4860.BevelDifferentialGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4860,
        )

        return self.__parent__._cast(
            _4860.BevelDifferentialGearSetCompoundModalAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4861.BevelDifferentialPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4861,
        )

        return self.__parent__._cast(
            _4861.BevelDifferentialPlanetGearCompoundModalAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4862.BevelDifferentialSunGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4862,
        )

        return self.__parent__._cast(
            _4862.BevelDifferentialSunGearCompoundModalAnalysis
        )

    @property
    def bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4863.BevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4863,
        )

        return self.__parent__._cast(_4863.BevelGearCompoundModalAnalysis)

    @property
    def bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4865.BevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4865,
        )

        return self.__parent__._cast(_4865.BevelGearSetCompoundModalAnalysis)

    @property
    def bolt_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4866.BoltCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4866,
        )

        return self.__parent__._cast(_4866.BoltCompoundModalAnalysis)

    @property
    def bolted_joint_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4867.BoltedJointCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4867,
        )

        return self.__parent__._cast(_4867.BoltedJointCompoundModalAnalysis)

    @property
    def clutch_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4868.ClutchCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4868,
        )

        return self.__parent__._cast(_4868.ClutchCompoundModalAnalysis)

    @property
    def clutch_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ClutchHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4870,
        )

        return self.__parent__._cast(_4870.ClutchHalfCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4872.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4872,
        )

        return self.__parent__._cast(_4872.ComponentCompoundModalAnalysis)

    @property
    def concept_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4873.ConceptCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4873,
        )

        return self.__parent__._cast(_4873.ConceptCouplingCompoundModalAnalysis)

    @property
    def concept_coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConceptCouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4875,
        )

        return self.__parent__._cast(_4875.ConceptCouplingHalfCompoundModalAnalysis)

    @property
    def concept_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4876.ConceptGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4876,
        )

        return self.__parent__._cast(_4876.ConceptGearCompoundModalAnalysis)

    @property
    def concept_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4878.ConceptGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4878,
        )

        return self.__parent__._cast(_4878.ConceptGearSetCompoundModalAnalysis)

    @property
    def conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4879.ConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4879,
        )

        return self.__parent__._cast(_4879.ConicalGearCompoundModalAnalysis)

    @property
    def conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4881.ConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4881,
        )

        return self.__parent__._cast(_4881.ConicalGearSetCompoundModalAnalysis)

    @property
    def connector_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4883.ConnectorCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4883,
        )

        return self.__parent__._cast(_4883.ConnectorCompoundModalAnalysis)

    @property
    def coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4884.CouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4884,
        )

        return self.__parent__._cast(_4884.CouplingCompoundModalAnalysis)

    @property
    def coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4886.CouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4886,
        )

        return self.__parent__._cast(_4886.CouplingHalfCompoundModalAnalysis)

    @property
    def cvt_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4888.CVTCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4888,
        )

        return self.__parent__._cast(_4888.CVTCompoundModalAnalysis)

    @property
    def cvt_pulley_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4889.CVTPulleyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4889,
        )

        return self.__parent__._cast(_4889.CVTPulleyCompoundModalAnalysis)

    @property
    def cycloidal_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4890.CycloidalAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4890,
        )

        return self.__parent__._cast(_4890.CycloidalAssemblyCompoundModalAnalysis)

    @property
    def cycloidal_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4892.CycloidalDiscCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4892,
        )

        return self.__parent__._cast(_4892.CycloidalDiscCompoundModalAnalysis)

    @property
    def cylindrical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4894.CylindricalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4894,
        )

        return self.__parent__._cast(_4894.CylindricalGearCompoundModalAnalysis)

    @property
    def cylindrical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4896.CylindricalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4896,
        )

        return self.__parent__._cast(_4896.CylindricalGearSetCompoundModalAnalysis)

    @property
    def cylindrical_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4897.CylindricalPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4897,
        )

        return self.__parent__._cast(_4897.CylindricalPlanetGearCompoundModalAnalysis)

    @property
    def datum_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4898.DatumCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4898,
        )

        return self.__parent__._cast(_4898.DatumCompoundModalAnalysis)

    @property
    def external_cad_model_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4899.ExternalCADModelCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4899,
        )

        return self.__parent__._cast(_4899.ExternalCADModelCompoundModalAnalysis)

    @property
    def face_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4900.FaceGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4900,
        )

        return self.__parent__._cast(_4900.FaceGearCompoundModalAnalysis)

    @property
    def face_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4902.FaceGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4902,
        )

        return self.__parent__._cast(_4902.FaceGearSetCompoundModalAnalysis)

    @property
    def fe_part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4903.FEPartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4903,
        )

        return self.__parent__._cast(_4903.FEPartCompoundModalAnalysis)

    @property
    def flexible_pin_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4904.FlexiblePinAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4904,
        )

        return self.__parent__._cast(_4904.FlexiblePinAssemblyCompoundModalAnalysis)

    @property
    def gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4905.GearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4905,
        )

        return self.__parent__._cast(_4905.GearCompoundModalAnalysis)

    @property
    def gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4907.GearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4907,
        )

        return self.__parent__._cast(_4907.GearSetCompoundModalAnalysis)

    @property
    def guide_dxf_model_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4908.GuideDxfModelCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4908,
        )

        return self.__parent__._cast(_4908.GuideDxfModelCompoundModalAnalysis)

    @property
    def hypoid_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4909.HypoidGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4909,
        )

        return self.__parent__._cast(_4909.HypoidGearCompoundModalAnalysis)

    @property
    def hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4911.HypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4911,
        )

        return self.__parent__._cast(_4911.HypoidGearSetCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4913.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4913,
        )

        return self.__parent__._cast(
            _4913.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4915.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4915,
        )

        return self.__parent__._cast(
            _4915.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4916.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4916,
        )

        return self.__parent__._cast(
            _4916.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4918.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4918,
        )

        return self.__parent__._cast(
            _4918.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4919.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4919,
        )

        return self.__parent__._cast(
            _4919.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4921.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4921,
        )

        return self.__parent__._cast(
            _4921.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis
        )

    @property
    def mass_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4922.MassDiscCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4922,
        )

        return self.__parent__._cast(_4922.MassDiscCompoundModalAnalysis)

    @property
    def measurement_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4923.MeasurementComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4923,
        )

        return self.__parent__._cast(_4923.MeasurementComponentCompoundModalAnalysis)

    @property
    def microphone_array_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MicrophoneArrayCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4924,
        )

        return self.__parent__._cast(_4924.MicrophoneArrayCompoundModalAnalysis)

    @property
    def microphone_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4925.MicrophoneCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4925,
        )

        return self.__parent__._cast(_4925.MicrophoneCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.MountableComponentCompoundModalAnalysis)

    @property
    def oil_seal_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4927.OilSealCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4927,
        )

        return self.__parent__._cast(_4927.OilSealCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4929.PartToPartShearCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4929,
        )

        return self.__parent__._cast(_4929.PartToPartShearCouplingCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4931.PartToPartShearCouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4931,
        )

        return self.__parent__._cast(
            _4931.PartToPartShearCouplingHalfCompoundModalAnalysis
        )

    @property
    def planetary_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4933.PlanetaryGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4933,
        )

        return self.__parent__._cast(_4933.PlanetaryGearSetCompoundModalAnalysis)

    @property
    def planet_carrier_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4934.PlanetCarrierCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4934,
        )

        return self.__parent__._cast(_4934.PlanetCarrierCompoundModalAnalysis)

    @property
    def point_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4935.PointLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4935,
        )

        return self.__parent__._cast(_4935.PointLoadCompoundModalAnalysis)

    @property
    def power_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4936.PowerLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4936,
        )

        return self.__parent__._cast(_4936.PowerLoadCompoundModalAnalysis)

    @property
    def pulley_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4937.PulleyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4937,
        )

        return self.__parent__._cast(_4937.PulleyCompoundModalAnalysis)

    @property
    def ring_pins_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4938.RingPinsCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4938,
        )

        return self.__parent__._cast(_4938.RingPinsCompoundModalAnalysis)

    @property
    def rolling_ring_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4940.RollingRingAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4940,
        )

        return self.__parent__._cast(_4940.RollingRingAssemblyCompoundModalAnalysis)

    @property
    def rolling_ring_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4941.RollingRingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4941,
        )

        return self.__parent__._cast(_4941.RollingRingCompoundModalAnalysis)

    @property
    def root_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4943.RootAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4943,
        )

        return self.__parent__._cast(_4943.RootAssemblyCompoundModalAnalysis)

    @property
    def shaft_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4944.ShaftCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4944,
        )

        return self.__parent__._cast(_4944.ShaftCompoundModalAnalysis)

    @property
    def shaft_hub_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4945.ShaftHubConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4945,
        )

        return self.__parent__._cast(_4945.ShaftHubConnectionCompoundModalAnalysis)

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4947.SpecialisedAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4947,
        )

        return self.__parent__._cast(_4947.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4948.SpiralBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4948,
        )

        return self.__parent__._cast(_4948.SpiralBevelGearCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4950.SpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4950,
        )

        return self.__parent__._cast(_4950.SpiralBevelGearSetCompoundModalAnalysis)

    @property
    def spring_damper_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4951.SpringDamperCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4951,
        )

        return self.__parent__._cast(_4951.SpringDamperCompoundModalAnalysis)

    @property
    def spring_damper_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4953.SpringDamperHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4953,
        )

        return self.__parent__._cast(_4953.SpringDamperHalfCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4954.StraightBevelDiffGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4954,
        )

        return self.__parent__._cast(_4954.StraightBevelDiffGearCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4956.StraightBevelDiffGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4956,
        )

        return self.__parent__._cast(
            _4956.StraightBevelDiffGearSetCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4957.StraightBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4957,
        )

        return self.__parent__._cast(_4957.StraightBevelGearCompoundModalAnalysis)

    @property
    def straight_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4959.StraightBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4959,
        )

        return self.__parent__._cast(_4959.StraightBevelGearSetCompoundModalAnalysis)

    @property
    def straight_bevel_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4960.StraightBevelPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4960,
        )

        return self.__parent__._cast(_4960.StraightBevelPlanetGearCompoundModalAnalysis)

    @property
    def straight_bevel_sun_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4961.StraightBevelSunGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4961,
        )

        return self.__parent__._cast(_4961.StraightBevelSunGearCompoundModalAnalysis)

    @property
    def synchroniser_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4962.SynchroniserCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4962,
        )

        return self.__parent__._cast(_4962.SynchroniserCompoundModalAnalysis)

    @property
    def synchroniser_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4963.SynchroniserHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4963,
        )

        return self.__parent__._cast(_4963.SynchroniserHalfCompoundModalAnalysis)

    @property
    def synchroniser_part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4964.SynchroniserPartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4964,
        )

        return self.__parent__._cast(_4964.SynchroniserPartCompoundModalAnalysis)

    @property
    def synchroniser_sleeve_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4965.SynchroniserSleeveCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4965,
        )

        return self.__parent__._cast(_4965.SynchroniserSleeveCompoundModalAnalysis)

    @property
    def torque_converter_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4966.TorqueConverterCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4966,
        )

        return self.__parent__._cast(_4966.TorqueConverterCompoundModalAnalysis)

    @property
    def torque_converter_pump_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4968.TorqueConverterPumpCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4968,
        )

        return self.__parent__._cast(_4968.TorqueConverterPumpCompoundModalAnalysis)

    @property
    def torque_converter_turbine_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4969.TorqueConverterTurbineCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4969,
        )

        return self.__parent__._cast(_4969.TorqueConverterTurbineCompoundModalAnalysis)

    @property
    def unbalanced_mass_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4970.UnbalancedMassCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4970,
        )

        return self.__parent__._cast(_4970.UnbalancedMassCompoundModalAnalysis)

    @property
    def virtual_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4971.VirtualComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4971,
        )

        return self.__parent__._cast(_4971.VirtualComponentCompoundModalAnalysis)

    @property
    def worm_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4972.WormGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4972,
        )

        return self.__parent__._cast(_4972.WormGearCompoundModalAnalysis)

    @property
    def worm_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4974.WormGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4974,
        )

        return self.__parent__._cast(_4974.WormGearSetCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4975.ZerolBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4975,
        )

        return self.__parent__._cast(_4975.ZerolBevelGearCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4977.ZerolBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4977,
        )

        return self.__parent__._cast(_4977.ZerolBevelGearSetCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(self: "CastSelf") -> "PartCompoundModalAnalysis":
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
class PartCompoundModalAnalysis(_7720.PartCompoundAnalysis):
    """PartCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(self: "Self") -> "List[_4781.PartModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis]

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
    def component_analysis_cases_ready(self: "Self") -> "List[_4781.PartModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundModalAnalysis
        """
        return _Cast_PartCompoundModalAnalysis(self)
