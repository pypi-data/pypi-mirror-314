"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1127 import (
        CylindricalGearBiasModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1128 import (
        CylindricalGearCommonFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1129 import (
        CylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1130 import (
        CylindricalGearLeadModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1131 import (
        CylindricalGearLeadModificationAtProfilePosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1132 import (
        CylindricalGearMeshMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1133 import (
        CylindricalGearMeshMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1134 import (
        CylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1135 import (
        CylindricalGearMicroGeometryBase,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1136 import (
        CylindricalGearMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1137 import (
        CylindricalGearMicroGeometryMap,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1138 import (
        CylindricalGearMicroGeometryPerTooth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1139 import (
        CylindricalGearProfileModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1140 import (
        CylindricalGearProfileModificationAtFaceWidthPosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1141 import (
        CylindricalGearSetMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1142 import (
        CylindricalGearSetMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1143 import (
        CylindricalGearToothMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1144 import (
        CylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1145 import (
        CylindricalGearTriangularEndModificationAtOrientation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1146 import (
        DrawDefiningGearOrBoth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1147 import (
        GearAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1148 import (
        LeadFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1149 import (
        LeadModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1150 import (
        LeadReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1151 import (
        LeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1152 import (
        LeadSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1153 import (
        LinearCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1154 import (
        MeasuredMapDataTypes,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1155 import (
        MeshAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1156 import (
        MeshedCylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1157 import (
        MeshedCylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1158 import (
        MicroGeometryLeadToleranceChartView,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1159 import (
        MicroGeometryViewingOptions,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1160 import (
        ModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1161 import (
        ParabolicCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1162 import (
        ProfileFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1163 import (
        ProfileModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1164 import (
        ProfileReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1165 import (
        ProfileReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1166 import (
        ProfileSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1167 import (
        ReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1168 import (
        SingleCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1169 import (
        TotalLeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1170 import (
        TotalProfileReliefWithDeviation,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.micro_geometry._1127": [
            "CylindricalGearBiasModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1128": [
            "CylindricalGearCommonFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1129": [
            "CylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1130": [
            "CylindricalGearLeadModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1131": [
            "CylindricalGearLeadModificationAtProfilePosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1132": [
            "CylindricalGearMeshMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1133": [
            "CylindricalGearMeshMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1134": [
            "CylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1135": [
            "CylindricalGearMicroGeometryBase"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1136": [
            "CylindricalGearMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1137": [
            "CylindricalGearMicroGeometryMap"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1138": [
            "CylindricalGearMicroGeometryPerTooth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1139": [
            "CylindricalGearProfileModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1140": [
            "CylindricalGearProfileModificationAtFaceWidthPosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1141": [
            "CylindricalGearSetMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1142": [
            "CylindricalGearSetMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1143": [
            "CylindricalGearToothMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1144": [
            "CylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1145": [
            "CylindricalGearTriangularEndModificationAtOrientation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1146": [
            "DrawDefiningGearOrBoth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1147": [
            "GearAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1148": [
            "LeadFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1149": [
            "LeadModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1150": [
            "LeadReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1151": [
            "LeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1152": [
            "LeadSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1153": [
            "LinearCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1154": [
            "MeasuredMapDataTypes"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1155": [
            "MeshAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1156": [
            "MeshedCylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1157": [
            "MeshedCylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1158": [
            "MicroGeometryLeadToleranceChartView"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1159": [
            "MicroGeometryViewingOptions"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1160": [
            "ModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1161": [
            "ParabolicCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1162": [
            "ProfileFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1163": [
            "ProfileModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1164": [
            "ProfileReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1165": [
            "ProfileReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1166": [
            "ProfileSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1167": [
            "ReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1168": [
            "SingleCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1169": [
            "TotalLeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1170": [
            "TotalProfileReliefWithDeviation"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBiasModification",
    "CylindricalGearCommonFlankMicroGeometry",
    "CylindricalGearFlankMicroGeometry",
    "CylindricalGearLeadModification",
    "CylindricalGearLeadModificationAtProfilePosition",
    "CylindricalGearMeshMicroGeometry",
    "CylindricalGearMeshMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometry",
    "CylindricalGearMicroGeometryBase",
    "CylindricalGearMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometryMap",
    "CylindricalGearMicroGeometryPerTooth",
    "CylindricalGearProfileModification",
    "CylindricalGearProfileModificationAtFaceWidthPosition",
    "CylindricalGearSetMicroGeometry",
    "CylindricalGearSetMicroGeometryDutyCycle",
    "CylindricalGearToothMicroGeometry",
    "CylindricalGearTriangularEndModification",
    "CylindricalGearTriangularEndModificationAtOrientation",
    "DrawDefiningGearOrBoth",
    "GearAlignment",
    "LeadFormReliefWithDeviation",
    "LeadModificationForCustomer102CAD",
    "LeadReliefSpecificationForCustomer102",
    "LeadReliefWithDeviation",
    "LeadSlopeReliefWithDeviation",
    "LinearCylindricalGearTriangularEndModification",
    "MeasuredMapDataTypes",
    "MeshAlignment",
    "MeshedCylindricalGearFlankMicroGeometry",
    "MeshedCylindricalGearMicroGeometry",
    "MicroGeometryLeadToleranceChartView",
    "MicroGeometryViewingOptions",
    "ModificationForCustomer102CAD",
    "ParabolicCylindricalGearTriangularEndModification",
    "ProfileFormReliefWithDeviation",
    "ProfileModificationForCustomer102CAD",
    "ProfileReliefSpecificationForCustomer102",
    "ProfileReliefWithDeviation",
    "ProfileSlopeReliefWithDeviation",
    "ReliefWithDeviation",
    "SingleCylindricalGearTriangularEndModification",
    "TotalLeadReliefWithDeviation",
    "TotalProfileReliefWithDeviation",
)
