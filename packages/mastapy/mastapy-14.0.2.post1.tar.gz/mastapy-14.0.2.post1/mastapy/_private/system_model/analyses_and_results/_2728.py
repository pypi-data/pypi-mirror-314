"""MultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2709

_CONCEPT_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingConnectionLoadCase",
)
_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CouplingConnectionLoadCase",
)
_SPRING_DAMPER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperConnectionLoadCase",
)
_TORQUE_CONVERTER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterConnectionLoadCase",
)
_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelPlanetGearLoadCase",
)
_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelSunGearLoadCase",
)
_WORM_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearLoadCase"
)
_WORM_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearSetLoadCase"
)
_ZEROL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ZerolBevelGearLoadCase"
)
_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearSetLoadCase",
)
_CYCLOIDAL_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalAssemblyLoadCase",
)
_CYCLOIDAL_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CycloidalDiscLoadCase"
)
_RING_PINS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RingPinsLoadCase"
)
_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingLoadCase",
)
_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingHalfLoadCase",
)
_BELT_DRIVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltDriveLoadCase"
)
_CLUTCH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchLoadCase"
)
_CLUTCH_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchHalfLoadCase"
)
_CONCEPT_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptCouplingLoadCase"
)
_CONCEPT_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingHalfLoadCase",
)
_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingLoadCase"
)
_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)
_CVT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTLoadCase"
)
_CVT_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTPulleyLoadCase"
)
_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PulleyLoadCase"
)
_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftHubConnectionLoadCase",
)
_ROLLING_RING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RollingRingLoadCase"
)
_ROLLING_RING_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingAssemblyLoadCase",
)
_SPRING_DAMPER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpringDamperLoadCase"
)
_SPRING_DAMPER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperHalfLoadCase",
)
_SYNCHRONISER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SynchroniserLoadCase"
)
_SYNCHRONISER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserHalfLoadCase",
)
_SYNCHRONISER_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserPartLoadCase",
)
_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserSleeveLoadCase",
)
_TORQUE_CONVERTER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TorqueConverterLoadCase"
)
_TORQUE_CONVERTER_PUMP_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterPumpLoadCase",
)
_TORQUE_CONVERTER_TURBINE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterTurbineLoadCase",
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftToMountableComponentConnectionLoadCase",
)
_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CVTBeltConnectionLoadCase",
)
_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltConnectionLoadCase"
)
_COAXIAL_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CoaxialConnectionLoadCase",
)
_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectionLoadCase"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "InterMountableComponentConnectionLoadCase",
)
_PLANETARY_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryConnectionLoadCase",
)
_ROLLING_RING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingConnectionLoadCase",
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftToMountableComponentConnectionLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearMeshLoadCase",
)
_CONCEPT_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearMeshLoadCase"
)
_FACE_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearMeshLoadCase"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearMeshLoadCase",
)
_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearMeshLoadCase"
)
_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearMeshLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearMeshLoadCase",
)
_CYLINDRICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearMeshLoadCase",
)
_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearMeshLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
)
_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearMeshLoadCase",
)
_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearMeshLoadCase",
)
_WORM_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearMeshLoadCase"
)
_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearMeshLoadCase",
)
_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearMeshLoadCase"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscCentralBearingConnectionLoadCase",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscPlanetaryBearingConnectionLoadCase",
)
_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RingPinsToDiscConnectionLoadCase",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingConnectionLoadCase",
)
_CLUTCH_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ClutchConnectionLoadCase",
)
_ABSTRACT_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AbstractShaftLoadCase"
)
_MICROPHONE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneLoadCase"
)
_MICROPHONE_ARRAY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneArrayLoadCase"
)
_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractAssemblyLoadCase",
)
_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftOrHousingLoadCase",
)
_BEARING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BearingLoadCase"
)
_BOLT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltLoadCase"
)
_BOLTED_JOINT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltedJointLoadCase"
)
_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)
_CONNECTOR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectorLoadCase"
)
_DATUM_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "DatumLoadCase"
)
_EXTERNAL_CAD_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ExternalCADModelLoadCase",
)
_FE_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FEPartLoadCase"
)
_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "FlexiblePinAssemblyLoadCase",
)
_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AssemblyLoadCase"
)
_GUIDE_DXF_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GuideDxfModelLoadCase"
)
_MASS_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MassDiscLoadCase"
)
_MEASUREMENT_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MeasurementComponentLoadCase",
)
_MOUNTABLE_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MountableComponentLoadCase",
)
_OIL_SEAL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "OilSealLoadCase"
)
_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)
_PLANET_CARRIER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PlanetCarrierLoadCase"
)
_POINT_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PointLoadLoadCase"
)
_POWER_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PowerLoadLoadCase"
)
_ROOT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RootAssemblyLoadCase"
)
_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpecialisedAssemblyLoadCase",
)
_UNBALANCED_MASS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "UnbalancedMassLoadCase"
)
_VIRTUAL_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "VirtualComponentLoadCase",
)
_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ShaftLoadCase"
)
_CONCEPT_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearLoadCase"
)
_CONCEPT_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearSetLoadCase"
)
_FACE_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearLoadCase"
)
_FACE_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearSetLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearLoadCase",
)
_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialPlanetGearLoadCase",
)
_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialSunGearLoadCase",
)
_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearLoadCase"
)
_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearSetLoadCase"
)
_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearLoadCase"
)
_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearSetLoadCase"
)
_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CylindricalGearLoadCase"
)
_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetLoadCase",
)
_CYLINDRICAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalPlanetGearLoadCase",
)
_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)
_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearSetLoadCase"
)
_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearLoadCase"
)
_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearSetLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
)
_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryGearSetLoadCase",
)
_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpiralBevelGearLoadCase"
)
_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearSetLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearSetLoadCase",
)
_STRAIGHT_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearLoadCase",
)
_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearSetLoadCase",
)
_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "MultibodyDynamicsAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7727
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5505,
        _5506,
        _5507,
        _5508,
        _5509,
        _5510,
        _5511,
        _5513,
        _5515,
        _5517,
        _5518,
        _5519,
        _5520,
        _5521,
        _5522,
        _5523,
        _5524,
        _5525,
        _5526,
        _5527,
        _5528,
        _5529,
        _5530,
        _5531,
        _5533,
        _5534,
        _5535,
        _5536,
        _5537,
        _5538,
        _5539,
        _5540,
        _5541,
        _5542,
        _5543,
        _5544,
        _5545,
        _5546,
        _5547,
        _5548,
        _5549,
        _5550,
        _5551,
        _5552,
        _5553,
        _5554,
        _5555,
        _5556,
        _5557,
        _5558,
        _5559,
        _5560,
        _5561,
        _5562,
        _5563,
        _5564,
        _5565,
        _5566,
        _5567,
        _5569,
        _5570,
        _5571,
        _5572,
        _5573,
        _5574,
        _5579,
        _5580,
        _5581,
        _5582,
        _5583,
        _5584,
        _5585,
        _5586,
        _5587,
        _5588,
        _5589,
        _5593,
        _5594,
        _5595,
        _5596,
        _5598,
        _5599,
        _5600,
        _5601,
        _5602,
        _5603,
        _5604,
        _5605,
        _5606,
        _5607,
        _5608,
        _5609,
        _5610,
        _5611,
        _5612,
        _5613,
        _5614,
        _5617,
        _5618,
        _5619,
        _5621,
        _5622,
        _5623,
        _5624,
        _5626,
        _5627,
        _5628,
        _5629,
        _5630,
        _5631,
        _5632,
        _5633,
        _5634,
        _5635,
        _5636,
        _5637,
        _5638,
        _5639,
        _5640,
        _5641,
        _5643,
        _5644,
        _5646,
        _5647,
        _5648,
        _5650,
        _5651,
        _5652,
        _5653,
        _5654,
        _5655,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6959,
        _6960,
        _6961,
        _6962,
        _6966,
        _6967,
        _6968,
        _6971,
        _6972,
        _6973,
        _6974,
        _6975,
        _6976,
        _6977,
        _6978,
        _6979,
        _6980,
        _6981,
        _6982,
        _6983,
        _6984,
        _6985,
        _6986,
        _6987,
        _6989,
        _6990,
        _6991,
        _6992,
        _6993,
        _6994,
        _6995,
        _6996,
        _6997,
        _6999,
        _7001,
        _7002,
        _7003,
        _7004,
        _7005,
        _7006,
        _7007,
        _7008,
        _7009,
        _7010,
        _7011,
        _7012,
        _7013,
        _7014,
        _7016,
        _7018,
        _7019,
        _7022,
        _7036,
        _7037,
        _7038,
        _7039,
        _7040,
        _7041,
        _7043,
        _7045,
        _7048,
        _7049,
        _7058,
        _7059,
        _7060,
        _7064,
        _7065,
        _7066,
        _7067,
        _7068,
        _7069,
        _7070,
        _7071,
        _7072,
        _7073,
        _7074,
        _7075,
        _7077,
        _7078,
        _7079,
        _7081,
        _7083,
        _7084,
        _7085,
        _7086,
        _7087,
        _7088,
        _7090,
        _7093,
        _7094,
        _7095,
        _7098,
        _7099,
        _7100,
        _7101,
        _7102,
        _7103,
        _7104,
        _7105,
        _7106,
        _7107,
        _7108,
        _7109,
        _7110,
        _7111,
        _7112,
        _7113,
        _7114,
        _7115,
        _7116,
        _7117,
        _7118,
        _7119,
        _7120,
        _7121,
        _7122,
        _7123,
        _7124,
        _7125,
        _7127,
        _7128,
        _7129,
        _7130,
        _7135,
        _7136,
        _7137,
        _7138,
        _7139,
        _7140,
        _7141,
        _7142,
    )
    from mastapy._private.system_model.connections_and_sockets import (
        _2322,
        _2325,
        _2326,
        _2329,
        _2330,
        _2338,
        _2344,
        _2349,
        _2352,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2399,
        _2401,
        _2403,
        _2405,
        _2407,
        _2409,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2392,
        _2395,
        _2398,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2356,
        _2358,
        _2360,
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2372,
        _2375,
        _2376,
        _2377,
        _2380,
        _2382,
        _2384,
        _2386,
        _2388,
    )
    from mastapy._private.system_model.part_model import (
        _2491,
        _2492,
        _2493,
        _2494,
        _2497,
        _2500,
        _2501,
        _2502,
        _2505,
        _2506,
        _2510,
        _2511,
        _2512,
        _2513,
        _2520,
        _2521,
        _2522,
        _2523,
        _2524,
        _2526,
        _2528,
        _2529,
        _2531,
        _2532,
        _2535,
        _2537,
        _2538,
        _2540,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2638,
        _2640,
        _2641,
        _2643,
        _2644,
        _2646,
        _2647,
        _2649,
        _2650,
        _2651,
        _2652,
        _2654,
        _2660,
        _2661,
        _2662,
        _2667,
        _2668,
        _2669,
        _2671,
        _2672,
        _2673,
        _2674,
        _2675,
        _2677,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2629, _2630, _2631
    from mastapy._private.system_model.part_model.gears import (
        _2574,
        _2575,
        _2576,
        _2577,
        _2578,
        _2579,
        _2580,
        _2581,
        _2582,
        _2583,
        _2584,
        _2585,
        _2586,
        _2587,
        _2588,
        _2589,
        _2590,
        _2591,
        _2593,
        _2595,
        _2596,
        _2597,
        _2598,
        _2599,
        _2600,
        _2601,
        _2602,
        _2603,
        _2604,
        _2605,
        _2606,
        _2607,
        _2608,
        _2609,
        _2610,
        _2611,
        _2612,
        _2613,
        _2614,
        _2615,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2543

    Self = TypeVar("Self", bound="MultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="MultibodyDynamicsAnalysis._Cast_MultibodyDynamicsAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultibodyDynamicsAnalysis:
    """Special nested class for casting MultibodyDynamicsAnalysis to subclasses."""

    __parent__: "MultibodyDynamicsAnalysis"

    @property
    def single_analysis(self: "CastSelf") -> "_2709.SingleAnalysis":
        return self.__parent__._cast(_2709.SingleAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7727.MarshalByRefObjectPermanent":
        from mastapy._private import _7727

        return self.__parent__._cast(_7727.MarshalByRefObjectPermanent)

    @property
    def multibody_dynamics_analysis(self: "CastSelf") -> "MultibodyDynamicsAnalysis":
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
class MultibodyDynamicsAnalysis(_2709.SingleAnalysis):
    """MultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def results_for_concept_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_6991.ConceptCouplingConnectionLoadCase"
    ) -> "_5535.ConceptCouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling_connection(
        self: "Self", design_entity: "_2403.CouplingConnection"
    ) -> "_5546.CouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_7004.CouplingConnectionLoadCase"
    ) -> "_5546.CouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper_connection(
        self: "Self", design_entity: "_2407.SpringDamperConnection"
    ) -> "_5626.SpringDamperConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper_connection_load_case(
        self: "Self", design_entity_analysis: "_7111.SpringDamperConnectionLoadCase"
    ) -> "_5626.SpringDamperConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_connection(
        self: "Self", design_entity: "_2409.TorqueConverterConnection"
    ) -> "_5641.TorqueConverterConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_connection_load_case(
        self: "Self", design_entity_analysis: "_7127.TorqueConverterConnectionLoadCase"
    ) -> "_5641.TorqueConverterConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7120.StraightBevelPlanetGearLoadCase"
    ) -> "_5635.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2611.StraightBevelSunGear"
    ) -> "_5636.StraightBevelSunGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelSunGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_7121.StraightBevelSunGearLoadCase"
    ) -> "_5636.StraightBevelSunGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelSunGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear(
        self: "Self", design_entity: "_2612.WormGear"
    ) -> "_5651.WormGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear_load_case(
        self: "Self", design_entity_analysis: "_7137.WormGearLoadCase"
    ) -> "_5651.WormGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear_set(
        self: "Self", design_entity: "_2613.WormGearSet"
    ) -> "_5652.WormGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7139.WormGearSetLoadCase"
    ) -> "_5652.WormGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2614.ZerolBevelGear"
    ) -> "_5654.ZerolBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7140.ZerolBevelGearLoadCase"
    ) -> "_5654.ZerolBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2615.ZerolBevelGearSet"
    ) -> "_5655.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7142.ZerolBevelGearSetLoadCase"
    ) -> "_5655.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_assembly(
        self: "Self", design_entity: "_2629.CycloidalAssembly"
    ) -> "_5552.CycloidalAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_assembly_load_case(
        self: "Self", design_entity_analysis: "_7010.CycloidalAssemblyLoadCase"
    ) -> "_5552.CycloidalAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc(
        self: "Self", design_entity: "_2630.CycloidalDisc"
    ) -> "_5554.CycloidalDiscMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_load_case(
        self: "Self", design_entity_analysis: "_7012.CycloidalDiscLoadCase"
    ) -> "_5554.CycloidalDiscMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_ring_pins(
        self: "Self", design_entity: "_2631.RingPins"
    ) -> "_5609.RingPinsMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RingPinsMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_ring_pins_load_case(
        self: "Self", design_entity_analysis: "_7098.RingPinsLoadCase"
    ) -> "_5609.RingPinsMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RingPinsMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2651.PartToPartShearCoupling"
    ) -> "_5602.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_load_case(
        self: "Self", design_entity_analysis: "_7086.PartToPartShearCouplingLoadCase"
    ) -> "_5602.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2652.PartToPartShearCouplingHalf"
    ) -> "_5601.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half_load_case(
        self: "Self",
        design_entity_analysis: "_7085.PartToPartShearCouplingHalfLoadCase",
    ) -> "_5601.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_belt_drive(
        self: "Self", design_entity: "_2638.BeltDrive"
    ) -> "_5518.BeltDriveMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BeltDriveMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_belt_drive_load_case(
        self: "Self", design_entity_analysis: "_6974.BeltDriveLoadCase"
    ) -> "_5518.BeltDriveMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BeltDriveMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch(
        self: "Self", design_entity: "_2640.Clutch"
    ) -> "_5531.ClutchMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch_load_case(
        self: "Self", design_entity_analysis: "_6987.ClutchLoadCase"
    ) -> "_5531.ClutchMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch_half(
        self: "Self", design_entity: "_2641.ClutchHalf"
    ) -> "_5530.ClutchHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch_half_load_case(
        self: "Self", design_entity_analysis: "_6986.ClutchHalfLoadCase"
    ) -> "_5530.ClutchHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_coupling(
        self: "Self", design_entity: "_2643.ConceptCoupling"
    ) -> "_5537.ConceptCouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_coupling_load_case(
        self: "Self", design_entity_analysis: "_6993.ConceptCouplingLoadCase"
    ) -> "_5537.ConceptCouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_coupling_half(
        self: "Self", design_entity: "_2644.ConceptCouplingHalf"
    ) -> "_5536.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_6992.ConceptCouplingHalfLoadCase"
    ) -> "_5536.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling(
        self: "Self", design_entity: "_2646.Coupling"
    ) -> "_5548.CouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling_load_case(
        self: "Self", design_entity_analysis: "_7006.CouplingLoadCase"
    ) -> "_5548.CouplingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling_half(
        self: "Self", design_entity: "_2647.CouplingHalf"
    ) -> "_5547.CouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_7005.CouplingHalfLoadCase"
    ) -> "_5547.CouplingHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CouplingHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt(
        self: "Self", design_entity: "_2649.CVT"
    ) -> "_5550.CVTMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt_load_case(
        self: "Self", design_entity_analysis: "_7008.CVTLoadCase"
    ) -> "_5550.CVTMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt_pulley(
        self: "Self", design_entity: "_2650.CVTPulley"
    ) -> "_5551.CVTPulleyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTPulleyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt_pulley_load_case(
        self: "Self", design_entity_analysis: "_7009.CVTPulleyLoadCase"
    ) -> "_5551.CVTPulleyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTPulleyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_pulley(
        self: "Self", design_entity: "_2654.Pulley"
    ) -> "_5608.PulleyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PulleyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_pulley_load_case(
        self: "Self", design_entity_analysis: "_7095.PulleyLoadCase"
    ) -> "_5608.PulleyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PulleyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft_hub_connection(
        self: "Self", design_entity: "_2662.ShaftHubConnection"
    ) -> "_5617.ShaftHubConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftHubConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft_hub_connection_load_case(
        self: "Self", design_entity_analysis: "_7104.ShaftHubConnectionLoadCase"
    ) -> "_5617.ShaftHubConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftHubConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring(
        self: "Self", design_entity: "_2660.RollingRing"
    ) -> "_5613.RollingRingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring_load_case(
        self: "Self", design_entity_analysis: "_7102.RollingRingLoadCase"
    ) -> "_5613.RollingRingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2661.RollingRingAssembly"
    ) -> "_5611.RollingRingAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring_assembly_load_case(
        self: "Self", design_entity_analysis: "_7100.RollingRingAssemblyLoadCase"
    ) -> "_5611.RollingRingAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper(
        self: "Self", design_entity: "_2667.SpringDamper"
    ) -> "_5628.SpringDamperMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper_load_case(
        self: "Self", design_entity_analysis: "_7113.SpringDamperLoadCase"
    ) -> "_5628.SpringDamperMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper_half(
        self: "Self", design_entity: "_2668.SpringDamperHalf"
    ) -> "_5627.SpringDamperHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spring_damper_half_load_case(
        self: "Self", design_entity_analysis: "_7112.SpringDamperHalfLoadCase"
    ) -> "_5627.SpringDamperHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpringDamperHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser(
        self: "Self", design_entity: "_2669.Synchroniser"
    ) -> "_5638.SynchroniserMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_load_case(
        self: "Self", design_entity_analysis: "_7123.SynchroniserLoadCase"
    ) -> "_5638.SynchroniserMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_half(
        self: "Self", design_entity: "_2671.SynchroniserHalf"
    ) -> "_5637.SynchroniserHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserHalfMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_half_load_case(
        self: "Self", design_entity_analysis: "_7122.SynchroniserHalfLoadCase"
    ) -> "_5637.SynchroniserHalfMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserHalfMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_part(
        self: "Self", design_entity: "_2672.SynchroniserPart"
    ) -> "_5639.SynchroniserPartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserPartMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_part_load_case(
        self: "Self", design_entity_analysis: "_7124.SynchroniserPartLoadCase"
    ) -> "_5639.SynchroniserPartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserPartMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2673.SynchroniserSleeve"
    ) -> "_5640.SynchroniserSleeveMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserSleeveMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_synchroniser_sleeve_load_case(
        self: "Self", design_entity_analysis: "_7125.SynchroniserSleeveLoadCase"
    ) -> "_5640.SynchroniserSleeveMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SynchroniserSleeveMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter(
        self: "Self", design_entity: "_2674.TorqueConverter"
    ) -> "_5643.TorqueConverterMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_load_case(
        self: "Self", design_entity_analysis: "_7128.TorqueConverterLoadCase"
    ) -> "_5643.TorqueConverterMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_pump(
        self: "Self", design_entity: "_2675.TorqueConverterPump"
    ) -> "_5644.TorqueConverterPumpMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterPumpMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_pump_load_case(
        self: "Self", design_entity_analysis: "_7129.TorqueConverterPumpLoadCase"
    ) -> "_5644.TorqueConverterPumpMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterPumpMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_turbine(
        self: "Self", design_entity: "_2677.TorqueConverterTurbine"
    ) -> "_5646.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterTurbineMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_torque_converter_turbine_load_case(
        self: "Self", design_entity_analysis: "_7130.TorqueConverterTurbineLoadCase"
    ) -> "_5646.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterTurbineMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2352.ShaftToMountableComponentConnection"
    ) -> "_5619.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7106.ShaftToMountableComponentConnectionLoadCase",
    ) -> "_5619.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt_belt_connection(
        self: "Self", design_entity: "_2330.CVTBeltConnection"
    ) -> "_5549.CVTBeltConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTBeltConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cvt_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_7007.CVTBeltConnectionLoadCase"
    ) -> "_5549.CVTBeltConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CVTBeltConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_belt_connection(
        self: "Self", design_entity: "_2325.BeltConnection"
    ) -> "_5517.BeltConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BeltConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_6973.BeltConnectionLoadCase"
    ) -> "_5517.BeltConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BeltConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coaxial_connection(
        self: "Self", design_entity: "_2326.CoaxialConnection"
    ) -> "_5533.CoaxialConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CoaxialConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_coaxial_connection_load_case(
        self: "Self", design_entity_analysis: "_6989.CoaxialConnectionLoadCase"
    ) -> "_5533.CoaxialConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CoaxialConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_connection(
        self: "Self", design_entity: "_2329.Connection"
    ) -> "_5544.ConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_connection_load_case(
        self: "Self", design_entity_analysis: "_7002.ConnectionLoadCase"
    ) -> "_5544.ConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2338.InterMountableComponentConnection"
    ) -> "_5579.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InterMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_inter_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7064.InterMountableComponentConnectionLoadCase",
    ) -> "_5579.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InterMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planetary_connection(
        self: "Self", design_entity: "_2344.PlanetaryConnection"
    ) -> "_5603.PlanetaryConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetaryConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planetary_connection_load_case(
        self: "Self", design_entity_analysis: "_7087.PlanetaryConnectionLoadCase"
    ) -> "_5603.PlanetaryConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetaryConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring_connection(
        self: "Self", design_entity: "_2349.RollingRingConnection"
    ) -> "_5612.RollingRingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_rolling_ring_connection_load_case(
        self: "Self", design_entity_analysis: "_7101.RollingRingConnectionLoadCase"
    ) -> "_5612.RollingRingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RollingRingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2322.AbstractShaftToMountableComponentConnection"
    ) -> "_5508.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_6962.AbstractShaftToMountableComponentConnectionLoadCase",
    ) -> "_5508.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2358.BevelDifferentialGearMesh"
    ) -> "_5519.BevelDifferentialGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_6976.BevelDifferentialGearMeshLoadCase"
    ) -> "_5519.BevelDifferentialGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear_mesh(
        self: "Self", design_entity: "_2362.ConceptGearMesh"
    ) -> "_5538.ConceptGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_6995.ConceptGearMeshLoadCase"
    ) -> "_5538.ConceptGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear_mesh(
        self: "Self", design_entity: "_2368.FaceGearMesh"
    ) -> "_5562.FaceGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7038.FaceGearMeshLoadCase"
    ) -> "_5562.FaceGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2382.StraightBevelDiffGearMesh"
    ) -> "_5629.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7115.StraightBevelDiffGearMeshLoadCase"
    ) -> "_5629.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2360.BevelGearMesh"
    ) -> "_5524.BevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_6981.BevelGearMeshLoadCase"
    ) -> "_5524.BevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear_mesh(
        self: "Self", design_entity: "_2364.ConicalGearMesh"
    ) -> "_5541.ConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_6999.ConicalGearMeshLoadCase"
    ) -> "_5541.ConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2356.AGMAGleasonConicalGearMesh"
    ) -> "_5509.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_6967.AGMAGleasonConicalGearMeshLoadCase"
    ) -> "_5509.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2366.CylindricalGearMesh"
    ) -> "_5556.CylindricalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7016.CylindricalGearMeshLoadCase"
    ) -> "_5556.CylindricalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2372.HypoidGearMesh"
    ) -> "_5572.HypoidGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7059.HypoidGearMeshLoadCase"
    ) -> "_5572.HypoidGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2375.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "_5580.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7066.KlingelnbergCycloPalloidConicalGearMeshLoadCase",
    ) -> "_5580.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2376.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> "_5583.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7069.KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
    ) -> "_5583.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2377.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "_5586.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7072.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
    ) -> "_5586.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2380.SpiralBevelGearMesh"
    ) -> "_5622.SpiralBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7109.SpiralBevelGearMeshLoadCase"
    ) -> "_5622.SpiralBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2384.StraightBevelGearMesh"
    ) -> "_5632.StraightBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7118.StraightBevelGearMeshLoadCase"
    ) -> "_5632.StraightBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear_mesh(
        self: "Self", design_entity: "_2386.WormGearMesh"
    ) -> "_5650.WormGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_worm_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7138.WormGearMeshLoadCase"
    ) -> "_5650.WormGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WormGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2388.ZerolBevelGearMesh"
    ) -> "_5653.ZerolBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7141.ZerolBevelGearMeshLoadCase"
    ) -> "_5653.ZerolBevelGearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear_mesh(
        self: "Self", design_entity: "_2370.GearMesh"
    ) -> "_5567.GearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7045.GearMeshLoadCase"
    ) -> "_5567.GearMeshMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2392.CycloidalDiscCentralBearingConnection"
    ) -> "_5553.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7011.CycloidalDiscCentralBearingConnectionLoadCase",
    ) -> "_5553.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2395.CycloidalDiscPlanetaryBearingConnection"
    ) -> "_5555.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7013.CycloidalDiscPlanetaryBearingConnectionLoadCase",
    ) -> "_5555.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2398.RingPinsToDiscConnection"
    ) -> "_5610.RingPinsToDiscConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RingPinsToDiscConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection_load_case(
        self: "Self", design_entity_analysis: "_7099.RingPinsToDiscConnectionLoadCase"
    ) -> "_5610.RingPinsToDiscConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RingPinsToDiscConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2405.PartToPartShearCouplingConnection"
    ) -> "_5600.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7084.PartToPartShearCouplingConnectionLoadCase",
    ) -> "_5600.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch_connection(
        self: "Self", design_entity: "_2399.ClutchConnection"
    ) -> "_5529.ClutchConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_clutch_connection_load_case(
        self: "Self", design_entity_analysis: "_6985.ClutchConnectionLoadCase"
    ) -> "_5529.ClutchConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_coupling_connection(
        self: "Self", design_entity: "_2401.ConceptCouplingConnection"
    ) -> "_5535.ConceptCouplingConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptCouplingConnectionMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft(
        self: "Self", design_entity: "_2493.AbstractShaft"
    ) -> "_5506.AbstractShaftMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_load_case(
        self: "Self", design_entity_analysis: "_6960.AbstractShaftLoadCase"
    ) -> "_5506.AbstractShaftMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_microphone(
        self: "Self", design_entity: "_2522.Microphone"
    ) -> "_5595.MicrophoneMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MicrophoneMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_microphone_load_case(
        self: "Self", design_entity_analysis: "_7078.MicrophoneLoadCase"
    ) -> "_5595.MicrophoneMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MicrophoneMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_microphone_array(
        self: "Self", design_entity: "_2523.MicrophoneArray"
    ) -> "_5594.MicrophoneArrayMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MicrophoneArrayMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_microphone_array_load_case(
        self: "Self", design_entity_analysis: "_7077.MicrophoneArrayLoadCase"
    ) -> "_5594.MicrophoneArrayMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MicrophoneArrayMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_assembly(
        self: "Self", design_entity: "_2492.AbstractAssembly"
    ) -> "_5505.AbstractAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_assembly_load_case(
        self: "Self", design_entity_analysis: "_6959.AbstractAssemblyLoadCase"
    ) -> "_5505.AbstractAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2494.AbstractShaftOrHousing"
    ) -> "_5507.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftOrHousingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing_load_case(
        self: "Self", design_entity_analysis: "_6961.AbstractShaftOrHousingLoadCase"
    ) -> "_5507.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftOrHousingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bearing(
        self: "Self", design_entity: "_2497.Bearing"
    ) -> "_5515.BearingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bearing_load_case(
        self: "Self", design_entity_analysis: "_6972.BearingLoadCase"
    ) -> "_5515.BearingMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BearingMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bolt(
        self: "Self", design_entity: "_2500.Bolt"
    ) -> "_5528.BoltMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BoltMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bolt_load_case(
        self: "Self", design_entity_analysis: "_6984.BoltLoadCase"
    ) -> "_5528.BoltMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BoltMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bolted_joint(
        self: "Self", design_entity: "_2501.BoltedJoint"
    ) -> "_5527.BoltedJointMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BoltedJointMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bolted_joint_load_case(
        self: "Self", design_entity_analysis: "_6983.BoltedJointLoadCase"
    ) -> "_5527.BoltedJointMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BoltedJointMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_component(
        self: "Self", design_entity: "_2502.Component"
    ) -> "_5534.ComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ComponentMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_component_load_case(
        self: "Self", design_entity_analysis: "_6990.ComponentLoadCase"
    ) -> "_5534.ComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ComponentMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_connector(
        self: "Self", design_entity: "_2505.Connector"
    ) -> "_5545.ConnectorMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConnectorMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_connector_load_case(
        self: "Self", design_entity_analysis: "_7003.ConnectorLoadCase"
    ) -> "_5545.ConnectorMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConnectorMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_datum(
        self: "Self", design_entity: "_2506.Datum"
    ) -> "_5560.DatumMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.DatumMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_datum_load_case(
        self: "Self", design_entity_analysis: "_7022.DatumLoadCase"
    ) -> "_5560.DatumMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.DatumMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_external_cad_model(
        self: "Self", design_entity: "_2510.ExternalCADModel"
    ) -> "_5561.ExternalCADModelMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ExternalCADModelMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_external_cad_model_load_case(
        self: "Self", design_entity_analysis: "_7036.ExternalCADModelLoadCase"
    ) -> "_5561.ExternalCADModelMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ExternalCADModelMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_fe_part(
        self: "Self", design_entity: "_2511.FEPart"
    ) -> "_5565.FEPartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FEPartMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_fe_part_load_case(
        self: "Self", design_entity_analysis: "_7040.FEPartLoadCase"
    ) -> "_5565.FEPartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FEPartMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2512.FlexiblePinAssembly"
    ) -> "_5566.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FlexiblePinAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_flexible_pin_assembly_load_case(
        self: "Self", design_entity_analysis: "_7041.FlexiblePinAssemblyLoadCase"
    ) -> "_5566.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FlexiblePinAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_assembly(
        self: "Self", design_entity: "_2491.Assembly"
    ) -> "_5513.AssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_assembly_load_case(
        self: "Self", design_entity_analysis: "_6971.AssemblyLoadCase"
    ) -> "_5513.AssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_guide_dxf_model(
        self: "Self", design_entity: "_2513.GuideDxfModel"
    ) -> "_5571.GuideDxfModelMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GuideDxfModelMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_guide_dxf_model_load_case(
        self: "Self", design_entity_analysis: "_7049.GuideDxfModelLoadCase"
    ) -> "_5571.GuideDxfModelMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GuideDxfModelMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_mass_disc(
        self: "Self", design_entity: "_2520.MassDisc"
    ) -> "_5589.MassDiscMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MassDiscMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_mass_disc_load_case(
        self: "Self", design_entity_analysis: "_7074.MassDiscLoadCase"
    ) -> "_5589.MassDiscMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MassDiscMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_measurement_component(
        self: "Self", design_entity: "_2521.MeasurementComponent"
    ) -> "_5593.MeasurementComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MeasurementComponentMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_measurement_component_load_case(
        self: "Self", design_entity_analysis: "_7075.MeasurementComponentLoadCase"
    ) -> "_5593.MeasurementComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MeasurementComponentMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_mountable_component(
        self: "Self", design_entity: "_2524.MountableComponent"
    ) -> "_5596.MountableComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MountableComponentMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_mountable_component_load_case(
        self: "Self", design_entity_analysis: "_7079.MountableComponentLoadCase"
    ) -> "_5596.MountableComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MountableComponentMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_oil_seal(
        self: "Self", design_entity: "_2526.OilSeal"
    ) -> "_5598.OilSealMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.OilSealMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_oil_seal_load_case(
        self: "Self", design_entity_analysis: "_7081.OilSealLoadCase"
    ) -> "_5598.OilSealMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.OilSealMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part(
        self: "Self", design_entity: "_2528.Part"
    ) -> "_5599.PartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_part_load_case(
        self: "Self", design_entity_analysis: "_7083.PartLoadCase"
    ) -> "_5599.PartMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PartMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planet_carrier(
        self: "Self", design_entity: "_2529.PlanetCarrier"
    ) -> "_5605.PlanetCarrierMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetCarrierMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planet_carrier_load_case(
        self: "Self", design_entity_analysis: "_7090.PlanetCarrierLoadCase"
    ) -> "_5605.PlanetCarrierMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetCarrierMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_point_load(
        self: "Self", design_entity: "_2531.PointLoad"
    ) -> "_5606.PointLoadMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PointLoadMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_point_load_load_case(
        self: "Self", design_entity_analysis: "_7093.PointLoadLoadCase"
    ) -> "_5606.PointLoadMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PointLoadMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_power_load(
        self: "Self", design_entity: "_2532.PowerLoad"
    ) -> "_5607.PowerLoadMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PowerLoadMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_power_load_load_case(
        self: "Self", design_entity_analysis: "_7094.PowerLoadLoadCase"
    ) -> "_5607.PowerLoadMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PowerLoadMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_root_assembly(
        self: "Self", design_entity: "_2535.RootAssembly"
    ) -> "_5614.RootAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RootAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_root_assembly_load_case(
        self: "Self", design_entity_analysis: "_7103.RootAssemblyLoadCase"
    ) -> "_5614.RootAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.RootAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_specialised_assembly(
        self: "Self", design_entity: "_2537.SpecialisedAssembly"
    ) -> "_5621.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpecialisedAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_specialised_assembly_load_case(
        self: "Self", design_entity_analysis: "_7107.SpecialisedAssemblyLoadCase"
    ) -> "_5621.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpecialisedAssemblyMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_unbalanced_mass(
        self: "Self", design_entity: "_2538.UnbalancedMass"
    ) -> "_5647.UnbalancedMassMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.UnbalancedMassMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_unbalanced_mass_load_case(
        self: "Self", design_entity_analysis: "_7135.UnbalancedMassLoadCase"
    ) -> "_5647.UnbalancedMassMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.UnbalancedMassMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_virtual_component(
        self: "Self", design_entity: "_2540.VirtualComponent"
    ) -> "_5648.VirtualComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.VirtualComponentMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_virtual_component_load_case(
        self: "Self", design_entity_analysis: "_7136.VirtualComponentLoadCase"
    ) -> "_5648.VirtualComponentMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.VirtualComponentMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft(
        self: "Self", design_entity: "_2543.Shaft"
    ) -> "_5618.ShaftMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_shaft_load_case(
        self: "Self", design_entity_analysis: "_7105.ShaftLoadCase"
    ) -> "_5618.ShaftMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ShaftMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear(
        self: "Self", design_entity: "_2582.ConceptGear"
    ) -> "_5539.ConceptGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear_load_case(
        self: "Self", design_entity_analysis: "_6994.ConceptGearLoadCase"
    ) -> "_5539.ConceptGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear_set(
        self: "Self", design_entity: "_2583.ConceptGearSet"
    ) -> "_5540.ConceptGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_concept_gear_set_load_case(
        self: "Self", design_entity_analysis: "_6996.ConceptGearSetLoadCase"
    ) -> "_5540.ConceptGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConceptGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear(
        self: "Self", design_entity: "_2589.FaceGear"
    ) -> "_5563.FaceGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear_load_case(
        self: "Self", design_entity_analysis: "_7037.FaceGearLoadCase"
    ) -> "_5563.FaceGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear_set(
        self: "Self", design_entity: "_2590.FaceGearSet"
    ) -> "_5564.FaceGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_face_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7039.FaceGearSetLoadCase"
    ) -> "_5564.FaceGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.FaceGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2574.AGMAGleasonConicalGear"
    ) -> "_5510.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_6966.AGMAGleasonConicalGearLoadCase"
    ) -> "_5510.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2575.AGMAGleasonConicalGearSet"
    ) -> "_5511.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_6968.AGMAGleasonConicalGearSetLoadCase"
    ) -> "_5511.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear(
        self: "Self", design_entity: "_2576.BevelDifferentialGear"
    ) -> "_5520.BevelDifferentialGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_load_case(
        self: "Self", design_entity_analysis: "_6975.BevelDifferentialGearLoadCase"
    ) -> "_5520.BevelDifferentialGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2577.BevelDifferentialGearSet"
    ) -> "_5521.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_set_load_case(
        self: "Self", design_entity_analysis: "_6977.BevelDifferentialGearSetLoadCase"
    ) -> "_5521.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2578.BevelDifferentialPlanetGear"
    ) -> "_5522.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear_load_case(
        self: "Self",
        design_entity_analysis: "_6978.BevelDifferentialPlanetGearLoadCase",
    ) -> "_5522.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2579.BevelDifferentialSunGear"
    ) -> "_5523.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialSunGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_6979.BevelDifferentialSunGearLoadCase"
    ) -> "_5523.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelDifferentialSunGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear(
        self: "Self", design_entity: "_2580.BevelGear"
    ) -> "_5525.BevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_6980.BevelGearLoadCase"
    ) -> "_5525.BevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear_set(
        self: "Self", design_entity: "_2581.BevelGearSet"
    ) -> "_5526.BevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_6982.BevelGearSetLoadCase"
    ) -> "_5526.BevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear(
        self: "Self", design_entity: "_2584.ConicalGear"
    ) -> "_5542.ConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_6997.ConicalGearLoadCase"
    ) -> "_5542.ConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear_set(
        self: "Self", design_entity: "_2585.ConicalGearSet"
    ) -> "_5543.ConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7001.ConicalGearSetLoadCase"
    ) -> "_5543.ConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear(
        self: "Self", design_entity: "_2586.CylindricalGear"
    ) -> "_5557.CylindricalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_load_case(
        self: "Self", design_entity_analysis: "_7014.CylindricalGearLoadCase"
    ) -> "_5557.CylindricalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2587.CylindricalGearSet"
    ) -> "_5558.CylindricalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7018.CylindricalGearSetLoadCase"
    ) -> "_5558.CylindricalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2588.CylindricalPlanetGear"
    ) -> "_5559.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_cylindrical_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7019.CylindricalPlanetGearLoadCase"
    ) -> "_5559.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear(
        self: "Self", design_entity: "_2591.Gear"
    ) -> "_5569.GearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear_load_case(
        self: "Self", design_entity_analysis: "_7043.GearLoadCase"
    ) -> "_5569.GearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear_set(
        self: "Self", design_entity: "_2593.GearSet"
    ) -> "_5570.GearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7048.GearSetLoadCase"
    ) -> "_5570.GearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear(
        self: "Self", design_entity: "_2595.HypoidGear"
    ) -> "_5573.HypoidGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_load_case(
        self: "Self", design_entity_analysis: "_7058.HypoidGearLoadCase"
    ) -> "_5573.HypoidGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_set(
        self: "Self", design_entity: "_2596.HypoidGearSet"
    ) -> "_5574.HypoidGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7060.HypoidGearSetLoadCase"
    ) -> "_5574.HypoidGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.HypoidGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2597.KlingelnbergCycloPalloidConicalGear"
    ) -> "_5581.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7065.KlingelnbergCycloPalloidConicalGearLoadCase",
    ) -> "_5581.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2598.KlingelnbergCycloPalloidConicalGearSet"
    ) -> "_5582.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7067.KlingelnbergCycloPalloidConicalGearSetLoadCase",
    ) -> "_5582.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2599.KlingelnbergCycloPalloidHypoidGear"
    ) -> "_5584.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7068.KlingelnbergCycloPalloidHypoidGearLoadCase",
    ) -> "_5584.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2600.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> "_5585.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7070.KlingelnbergCycloPalloidHypoidGearSetLoadCase",
    ) -> "_5585.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2601.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "_5587.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7071.KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
    ) -> "_5587.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2602.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "_5588.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7073.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
    ) -> "_5588.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planetary_gear_set(
        self: "Self", design_entity: "_2603.PlanetaryGearSet"
    ) -> "_5604.PlanetaryGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetaryGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_planetary_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7088.PlanetaryGearSetLoadCase"
    ) -> "_5604.PlanetaryGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.PlanetaryGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2604.SpiralBevelGear"
    ) -> "_5623.SpiralBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7108.SpiralBevelGearLoadCase"
    ) -> "_5623.SpiralBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2605.SpiralBevelGearSet"
    ) -> "_5624.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7110.SpiralBevelGearSetLoadCase"
    ) -> "_5624.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SpiralBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2606.StraightBevelDiffGear"
    ) -> "_5630.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_load_case(
        self: "Self", design_entity_analysis: "_7114.StraightBevelDiffGearLoadCase"
    ) -> "_5630.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2607.StraightBevelDiffGearSet"
    ) -> "_5631.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7116.StraightBevelDiffGearSetLoadCase"
    ) -> "_5631.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear(
        self: "Self", design_entity: "_2608.StraightBevelGear"
    ) -> "_5633.StraightBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7117.StraightBevelGearLoadCase"
    ) -> "_5633.StraightBevelGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2609.StraightBevelGearSet"
    ) -> "_5634.StraightBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7119.StraightBevelGearSetLoadCase"
    ) -> "_5634.StraightBevelGearSetMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelGearSetMultibodyDynamicsAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2610.StraightBevelPlanetGear"
    ) -> "_5635.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelPlanetGearMultibodyDynamicsAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MultibodyDynamicsAnalysis
        """
        return _Cast_MultibodyDynamicsAnalysis(self)
