"""PartLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2746
from mastapy._private.system_model.analyses_and_results.static_loads import _6957, _7050

_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1430
    from mastapy._private.system_model.analyses_and_results import _2740, _2742
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6958,
        _6959,
        _6960,
        _6961,
        _6966,
        _6968,
        _6971,
        _6972,
        _6974,
        _6975,
        _6977,
        _6978,
        _6979,
        _6980,
        _6982,
        _6983,
        _6984,
        _6986,
        _6987,
        _6990,
        _6992,
        _6993,
        _6994,
        _6996,
        _6997,
        _7001,
        _7003,
        _7005,
        _7006,
        _7008,
        _7009,
        _7010,
        _7012,
        _7014,
        _7018,
        _7019,
        _7022,
        _7036,
        _7037,
        _7039,
        _7040,
        _7041,
        _7043,
        _7048,
        _7049,
        _7058,
        _7060,
        _7065,
        _7067,
        _7068,
        _7070,
        _7071,
        _7073,
        _7074,
        _7075,
        _7077,
        _7078,
        _7079,
        _7081,
        _7085,
        _7086,
        _7088,
        _7090,
        _7093,
        _7094,
        _7095,
        _7098,
        _7100,
        _7102,
        _7103,
        _7104,
        _7105,
        _7107,
        _7108,
        _7110,
        _7112,
        _7113,
        _7114,
        _7116,
        _7117,
        _7119,
        _7120,
        _7121,
        _7122,
        _7123,
        _7124,
        _7125,
        _7128,
        _7129,
        _7130,
        _7135,
        _7136,
        _7137,
        _7139,
        _7140,
        _7142,
    )
    from mastapy._private.system_model.part_model import _2528

    Self = TypeVar("Self", bound="PartLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PartLoadCase._Cast_PartLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartLoadCase:
    """Special nested class for casting PartLoadCase to subclasses."""

    __parent__: "PartLoadCase"

    @property
    def part_analysis(self: "CastSelf") -> "_2746.PartAnalysis":
        return self.__parent__._cast(_2746.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2742.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2742

        return self.__parent__._cast(_2742.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2740.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntityAnalysis)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_6960.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6960,
        )

        return self.__parent__._cast(_6960.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6961.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6966.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6966,
        )

        return self.__parent__._cast(_6966.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6968.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6968,
        )

        return self.__parent__._cast(_6968.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_6971.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6971,
        )

        return self.__parent__._cast(_6971.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_6972.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_6974.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6974,
        )

        return self.__parent__._cast(_6974.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6975.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6977.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6978.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6978,
        )

        return self.__parent__._cast(_6978.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6979.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6979,
        )

        return self.__parent__._cast(_6979.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6980.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6980,
        )

        return self.__parent__._cast(_6980.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_6982.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_6983.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6983,
        )

        return self.__parent__._cast(_6983.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_6984.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6984,
        )

        return self.__parent__._cast(_6984.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_6986.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6986,
        )

        return self.__parent__._cast(_6986.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_6987.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6990.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6992.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6993.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6993,
        )

        return self.__parent__._cast(_6993.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6994.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6994,
        )

        return self.__parent__._cast(_6994.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6996.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6996,
        )

        return self.__parent__._cast(_6996.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6997.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6997,
        )

        return self.__parent__._cast(_6997.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7001.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7001,
        )

        return self.__parent__._cast(_7001.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_7003.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7003,
        )

        return self.__parent__._cast(_7003.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7005.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7005,
        )

        return self.__parent__._cast(_7005.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7006.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7006,
        )

        return self.__parent__._cast(_7006.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7008.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7008,
        )

        return self.__parent__._cast(_7008.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7009.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7009,
        )

        return self.__parent__._cast(_7009.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7010.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7010,
        )

        return self.__parent__._cast(_7010.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7012.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7012,
        )

        return self.__parent__._cast(_7012.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7014.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7014,
        )

        return self.__parent__._cast(_7014.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7018.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7018,
        )

        return self.__parent__._cast(_7018.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7019.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7019,
        )

        return self.__parent__._cast(_7019.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7022.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7022,
        )

        return self.__parent__._cast(_7022.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7036.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7036,
        )

        return self.__parent__._cast(_7036.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7037.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7037,
        )

        return self.__parent__._cast(_7037.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7039.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7039,
        )

        return self.__parent__._cast(_7039.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7040.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7040,
        )

        return self.__parent__._cast(_7040.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7041.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7041,
        )

        return self.__parent__._cast(_7041.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7043.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7048.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7048,
        )

        return self.__parent__._cast(_7048.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7049.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7049,
        )

        return self.__parent__._cast(_7049.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7058.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7058,
        )

        return self.__parent__._cast(_7058.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7060.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7060,
        )

        return self.__parent__._cast(_7060.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7065.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7065,
        )

        return self.__parent__._cast(_7065.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7067.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7067,
        )

        return self.__parent__._cast(
            _7067.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7068.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7068,
        )

        return self.__parent__._cast(_7068.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7070.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7070,
        )

        return self.__parent__._cast(
            _7070.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7071.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7071,
        )

        return self.__parent__._cast(
            _7071.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7073.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7073,
        )

        return self.__parent__._cast(
            _7073.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7074.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7074,
        )

        return self.__parent__._cast(_7074.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7075.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7075,
        )

        return self.__parent__._cast(_7075.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7077.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7077,
        )

        return self.__parent__._cast(_7077.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7078.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7078,
        )

        return self.__parent__._cast(_7078.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7079.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7079,
        )

        return self.__parent__._cast(_7079.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7081.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7081,
        )

        return self.__parent__._cast(_7081.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7085.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7085,
        )

        return self.__parent__._cast(_7085.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7086.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7086,
        )

        return self.__parent__._cast(_7086.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7088.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7090.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7090,
        )

        return self.__parent__._cast(_7090.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7093.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7094.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7094,
        )

        return self.__parent__._cast(_7094.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7095.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7095,
        )

        return self.__parent__._cast(_7095.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7098.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7098,
        )

        return self.__parent__._cast(_7098.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7100.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7102.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

        return self.__parent__._cast(_7102.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7103.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7103,
        )

        return self.__parent__._cast(_7103.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7104.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7104,
        )

        return self.__parent__._cast(_7104.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7105.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7107.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7108.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7110.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7112.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7113.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7113,
        )

        return self.__parent__._cast(_7113.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7117.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7119.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7120.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7121.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7121,
        )

        return self.__parent__._cast(_7121.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7122.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7122,
        )

        return self.__parent__._cast(_7122.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7123.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7124.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7124,
        )

        return self.__parent__._cast(_7124.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7125.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7128.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7128,
        )

        return self.__parent__._cast(_7128.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7129.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7129,
        )

        return self.__parent__._cast(_7129.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7130.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7130,
        )

        return self.__parent__._cast(_7130.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7135.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7136.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7136,
        )

        return self.__parent__._cast(_7136.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7137.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7139.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7139,
        )

        return self.__parent__._cast(_7139.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7140.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7140,
        )

        return self.__parent__._cast(_7140.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7142.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7142,
        )

        return self.__parent__._cast(_7142.ZerolBevelGearSetLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "PartLoadCase":
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
class PartLoadCase(_2746.PartAnalysis):
    """PartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitation_data_is_up_to_date(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDataIsUpToDate")

        if temp is None:
            return False

        return temp

    @property
    def harmonic_excitation_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]"""
        temp = pythonnet_property_get(self.wrapped, "HarmonicExcitationType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @harmonic_excitation_type.setter
    @enforce_parameter_types
    def harmonic_excitation_type(
        self: "Self", value: "_7050.HarmonicExcitationType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "HarmonicExcitationType", value)

    @property
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "_6957.StaticLoadCase"
    ) -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            value,
        )

    @property
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            bool(value) if value is not None else False,
        )

    @property
    def component_design(self: "Self") -> "_2528.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def static_load_case(self: "Self") -> "_6957.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: "Self") -> "_6958.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def clear_user_specified_excitation_data_for_this_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForThisLoadCase"
        )

    def get_harmonic_load_data_for_import(self: "Self") -> "_1430.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PartLoadCase
        """
        return _Cast_PartLoadCase(self)
