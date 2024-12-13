"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1515 import AxialLoadType
    from mastapy._private.bolts._1516 import BoltedJointMaterial
    from mastapy._private.bolts._1517 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1518 import BoltGeometry
    from mastapy._private.bolts._1519 import BoltGeometryDatabase
    from mastapy._private.bolts._1520 import BoltMaterial
    from mastapy._private.bolts._1521 import BoltMaterialDatabase
    from mastapy._private.bolts._1522 import BoltSection
    from mastapy._private.bolts._1523 import BoltShankType
    from mastapy._private.bolts._1524 import BoltTypes
    from mastapy._private.bolts._1525 import ClampedSection
    from mastapy._private.bolts._1526 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1527 import DetailedBoltDesign
    from mastapy._private.bolts._1528 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1529 import HeadCapTypes
    from mastapy._private.bolts._1530 import JointGeometries
    from mastapy._private.bolts._1531 import JointTypes
    from mastapy._private.bolts._1532 import LoadedBolt
    from mastapy._private.bolts._1533 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1534 import StandardSizes
    from mastapy._private.bolts._1535 import StrengthGrades
    from mastapy._private.bolts._1536 import ThreadTypes
    from mastapy._private.bolts._1537 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1515": ["AxialLoadType"],
        "_private.bolts._1516": ["BoltedJointMaterial"],
        "_private.bolts._1517": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1518": ["BoltGeometry"],
        "_private.bolts._1519": ["BoltGeometryDatabase"],
        "_private.bolts._1520": ["BoltMaterial"],
        "_private.bolts._1521": ["BoltMaterialDatabase"],
        "_private.bolts._1522": ["BoltSection"],
        "_private.bolts._1523": ["BoltShankType"],
        "_private.bolts._1524": ["BoltTypes"],
        "_private.bolts._1525": ["ClampedSection"],
        "_private.bolts._1526": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1527": ["DetailedBoltDesign"],
        "_private.bolts._1528": ["DetailedBoltedJointDesign"],
        "_private.bolts._1529": ["HeadCapTypes"],
        "_private.bolts._1530": ["JointGeometries"],
        "_private.bolts._1531": ["JointTypes"],
        "_private.bolts._1532": ["LoadedBolt"],
        "_private.bolts._1533": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1534": ["StandardSizes"],
        "_private.bolts._1535": ["StrengthGrades"],
        "_private.bolts._1536": ["ThreadTypes"],
        "_private.bolts._1537": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
