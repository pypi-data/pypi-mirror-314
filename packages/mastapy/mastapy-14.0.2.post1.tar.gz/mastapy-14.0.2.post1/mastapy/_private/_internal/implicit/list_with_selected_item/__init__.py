"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

if TYPE_CHECKING:
    from .abstract_periodic_excitation_detail import (
        ListWithSelectedItem_AbstractPeriodicExcitationDetail,
    )
    from .acoustic_analysis_setup import ListWithSelectedItem_AcousticAnalysisSetup
    from .active_gear_set_design_selection_group import (
        ListWithSelectedItem_ActiveGearSetDesignSelectionGroup,
    )
    from .cms_element_face_group import ListWithSelectedItem_CMSElementFaceGroup
    from .column_title import ListWithSelectedItem_ColumnTitle
    from .component import ListWithSelectedItem_Component
    from .concentric_part_group import ListWithSelectedItem_ConcentricPartGroup
    from .conical_set_manufacturing_config import (
        ListWithSelectedItem_ConicalSetManufacturingConfig,
    )
    from .cylindrical_gear import ListWithSelectedItem_CylindricalGear
    from .cylindrical_gear_load_distribution_analysis import (
        ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis,
    )
    from .cylindrical_gear_mesh_load_distribution_analysis import (
        ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis,
    )
    from .cylindrical_gear_set import ListWithSelectedItem_CylindricalGearSet
    from .cylindrical_gear_system_deflection import (
        ListWithSelectedItem_CylindricalGearSystemDeflection,
    )
    from .cylindrical_set_manufacturing_config import (
        ListWithSelectedItem_CylindricalSetManufacturingConfig,
    )
    from .datum import ListWithSelectedItem_Datum
    from .design_state import ListWithSelectedItem_DesignState
    from .duty_cycle import ListWithSelectedItem_DutyCycle
    from .electric_machine_data_set import ListWithSelectedItem_ElectricMachineDataSet
    from .electric_machine_detail import ListWithSelectedItem_ElectricMachineDetail
    from .electric_machine_results import ListWithSelectedItem_ElectricMachineResults
    from .electric_machine_setup import ListWithSelectedItem_ElectricMachineSetup
    from .fe_link import ListWithSelectedItem_FELink
    from .fe_part import ListWithSelectedItem_FEPart
    from .fe_substructure import ListWithSelectedItem_FESubstructure
    from .fe_substructure_node import ListWithSelectedItem_FESubstructureNode
    from .float import ListWithSelectedItem_float
    from .gear_mesh_system_deflection import (
        ListWithSelectedItem_GearMeshSystemDeflection,
    )
    from .gear_set import ListWithSelectedItem_GearSet
    from .gear_set_design import ListWithSelectedItem_GearSetDesign
    from .guide_dxf_model import ListWithSelectedItem_GuideDxfModel
    from .harmonic_analysis_with_varying_stiffness_static_load_case import (
        ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase,
    )
    from .int import ListWithSelectedItem_int
    from .measurement_base import ListWithSelectedItem_MeasurementBase
    from .microphone_array import ListWithSelectedItem_MicrophoneArray
    from .point_load import ListWithSelectedItem_PointLoad
    from .power_load import ListWithSelectedItem_PowerLoad
    from .result_location_selection_group import (
        ListWithSelectedItem_ResultLocationSelectionGroup,
    )
    from .rotor_skew_slice import ListWithSelectedItem_RotorSkewSlice
    from .rounded_order import ListWithSelectedItem_RoundedOrder
    from .shaft_hub_connection import ListWithSelectedItem_ShaftHubConnection
    from .static_load_case import ListWithSelectedItem_StaticLoadCase
    from .str import ListWithSelectedItem_str
    from .system_directory import ListWithSelectedItem_SystemDirectory
    from .t import ListWithSelectedItem_T
    from .t_part_analysis import ListWithSelectedItem_TPartAnalysis
    from .t_selectable_item import ListWithSelectedItem_TSelectableItem
    from .tuple_with_name import ListWithSelectedItem_TupleWithName
    from .unit import ListWithSelectedItem_Unit
else:
    import_structure = {
        "unit": ["ListWithSelectedItem_Unit"],
        "str": ["ListWithSelectedItem_str"],
        "int": ["ListWithSelectedItem_int"],
        "t": ["ListWithSelectedItem_T"],
        "cylindrical_gear_load_distribution_analysis": [
            "ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis"
        ],
        "cylindrical_gear_mesh_load_distribution_analysis": [
            "ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis"
        ],
        "cylindrical_set_manufacturing_config": [
            "ListWithSelectedItem_CylindricalSetManufacturingConfig"
        ],
        "conical_set_manufacturing_config": [
            "ListWithSelectedItem_ConicalSetManufacturingConfig"
        ],
        "electric_machine_setup": ["ListWithSelectedItem_ElectricMachineSetup"],
        "float": ["ListWithSelectedItem_float"],
        "electric_machine_results": ["ListWithSelectedItem_ElectricMachineResults"],
        "rotor_skew_slice": ["ListWithSelectedItem_RotorSkewSlice"],
        "system_directory": ["ListWithSelectedItem_SystemDirectory"],
        "measurement_base": ["ListWithSelectedItem_MeasurementBase"],
        "column_title": ["ListWithSelectedItem_ColumnTitle"],
        "active_gear_set_design_selection_group": [
            "ListWithSelectedItem_ActiveGearSetDesignSelectionGroup"
        ],
        "power_load": ["ListWithSelectedItem_PowerLoad"],
        "duty_cycle": ["ListWithSelectedItem_DutyCycle"],
        "abstract_periodic_excitation_detail": [
            "ListWithSelectedItem_AbstractPeriodicExcitationDetail"
        ],
        "tuple_with_name": ["ListWithSelectedItem_TupleWithName"],
        "harmonic_analysis_with_varying_stiffness_static_load_case": [
            "ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"
        ],
        "rounded_order": ["ListWithSelectedItem_RoundedOrder"],
        "gear_mesh_system_deflection": [
            "ListWithSelectedItem_GearMeshSystemDeflection"
        ],
        "gear_set": ["ListWithSelectedItem_GearSet"],
        "microphone_array": ["ListWithSelectedItem_MicrophoneArray"],
        "fe_substructure_node": ["ListWithSelectedItem_FESubstructureNode"],
        "fe_substructure": ["ListWithSelectedItem_FESubstructure"],
        "cms_element_face_group": ["ListWithSelectedItem_CMSElementFaceGroup"],
        "component": ["ListWithSelectedItem_Component"],
        "datum": ["ListWithSelectedItem_Datum"],
        "fe_link": ["ListWithSelectedItem_FELink"],
        "cylindrical_gear": ["ListWithSelectedItem_CylindricalGear"],
        "electric_machine_detail": ["ListWithSelectedItem_ElectricMachineDetail"],
        "guide_dxf_model": ["ListWithSelectedItem_GuideDxfModel"],
        "concentric_part_group": ["ListWithSelectedItem_ConcentricPartGroup"],
        "cylindrical_gear_set": ["ListWithSelectedItem_CylindricalGearSet"],
        "gear_set_design": ["ListWithSelectedItem_GearSetDesign"],
        "shaft_hub_connection": ["ListWithSelectedItem_ShaftHubConnection"],
        "t_selectable_item": ["ListWithSelectedItem_TSelectableItem"],
        "cylindrical_gear_system_deflection": [
            "ListWithSelectedItem_CylindricalGearSystemDeflection"
        ],
        "design_state": ["ListWithSelectedItem_DesignState"],
        "fe_part": ["ListWithSelectedItem_FEPart"],
        "t_part_analysis": ["ListWithSelectedItem_TPartAnalysis"],
        "acoustic_analysis_setup": ["ListWithSelectedItem_AcousticAnalysisSetup"],
        "result_location_selection_group": [
            "ListWithSelectedItem_ResultLocationSelectionGroup"
        ],
        "static_load_case": ["ListWithSelectedItem_StaticLoadCase"],
        "electric_machine_data_set": ["ListWithSelectedItem_ElectricMachineDataSet"],
        "point_load": ["ListWithSelectedItem_PointLoad"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ListWithSelectedItem_Unit",
    "ListWithSelectedItem_str",
    "ListWithSelectedItem_int",
    "ListWithSelectedItem_T",
    "ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis",
    "ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis",
    "ListWithSelectedItem_CylindricalSetManufacturingConfig",
    "ListWithSelectedItem_ConicalSetManufacturingConfig",
    "ListWithSelectedItem_ElectricMachineSetup",
    "ListWithSelectedItem_float",
    "ListWithSelectedItem_ElectricMachineResults",
    "ListWithSelectedItem_RotorSkewSlice",
    "ListWithSelectedItem_SystemDirectory",
    "ListWithSelectedItem_MeasurementBase",
    "ListWithSelectedItem_ColumnTitle",
    "ListWithSelectedItem_ActiveGearSetDesignSelectionGroup",
    "ListWithSelectedItem_PowerLoad",
    "ListWithSelectedItem_DutyCycle",
    "ListWithSelectedItem_AbstractPeriodicExcitationDetail",
    "ListWithSelectedItem_TupleWithName",
    "ListWithSelectedItem_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
    "ListWithSelectedItem_RoundedOrder",
    "ListWithSelectedItem_GearMeshSystemDeflection",
    "ListWithSelectedItem_GearSet",
    "ListWithSelectedItem_MicrophoneArray",
    "ListWithSelectedItem_FESubstructureNode",
    "ListWithSelectedItem_FESubstructure",
    "ListWithSelectedItem_CMSElementFaceGroup",
    "ListWithSelectedItem_Component",
    "ListWithSelectedItem_Datum",
    "ListWithSelectedItem_FELink",
    "ListWithSelectedItem_CylindricalGear",
    "ListWithSelectedItem_ElectricMachineDetail",
    "ListWithSelectedItem_GuideDxfModel",
    "ListWithSelectedItem_ConcentricPartGroup",
    "ListWithSelectedItem_CylindricalGearSet",
    "ListWithSelectedItem_GearSetDesign",
    "ListWithSelectedItem_ShaftHubConnection",
    "ListWithSelectedItem_TSelectableItem",
    "ListWithSelectedItem_CylindricalGearSystemDeflection",
    "ListWithSelectedItem_DesignState",
    "ListWithSelectedItem_FEPart",
    "ListWithSelectedItem_TPartAnalysis",
    "ListWithSelectedItem_AcousticAnalysisSetup",
    "ListWithSelectedItem_ResultLocationSelectionGroup",
    "ListWithSelectedItem_StaticLoadCase",
    "ListWithSelectedItem_ElectricMachineDataSet",
    "ListWithSelectedItem_PointLoad",
)
