"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines._1284 import AbstractStator
    from mastapy._private.electric_machines._1285 import AbstractToothAndSlot
    from mastapy._private.electric_machines._1286 import CADConductor
    from mastapy._private.electric_machines._1287 import CADElectricMachineDetail
    from mastapy._private.electric_machines._1288 import CADFieldWindingSpecification
    from mastapy._private.electric_machines._1289 import CADMagnetDetails
    from mastapy._private.electric_machines._1290 import CADMagnetsForLayer
    from mastapy._private.electric_machines._1291 import CADRotor
    from mastapy._private.electric_machines._1292 import CADStator
    from mastapy._private.electric_machines._1293 import CADToothAndSlot
    from mastapy._private.electric_machines._1294 import CADWoundFieldSynchronousRotor
    from mastapy._private.electric_machines._1295 import Coil
    from mastapy._private.electric_machines._1296 import CoilPositionInSlot
    from mastapy._private.electric_machines._1297 import CoolingDuctLayerSpecification
    from mastapy._private.electric_machines._1298 import CoolingDuctShape
    from mastapy._private.electric_machines._1299 import (
        CoreLossBuildFactorSpecificationMethod,
    )
    from mastapy._private.electric_machines._1300 import CoreLossCoefficients
    from mastapy._private.electric_machines._1301 import DoubleLayerWindingSlotPositions
    from mastapy._private.electric_machines._1302 import DQAxisConvention
    from mastapy._private.electric_machines._1303 import Eccentricity
    from mastapy._private.electric_machines._1304 import ElectricMachineDetail
    from mastapy._private.electric_machines._1305 import (
        ElectricMachineDetailInitialInformation,
    )
    from mastapy._private.electric_machines._1306 import ElectricMachineGroup
    from mastapy._private.electric_machines._1307 import (
        ElectricMachineMechanicalAnalysisMeshingOptions,
    )
    from mastapy._private.electric_machines._1308 import ElectricMachineMeshingOptions
    from mastapy._private.electric_machines._1309 import (
        ElectricMachineMeshingOptionsBase,
    )
    from mastapy._private.electric_machines._1310 import ElectricMachineSetup
    from mastapy._private.electric_machines._1311 import ElectricMachineType
    from mastapy._private.electric_machines._1312 import FieldWindingSpecification
    from mastapy._private.electric_machines._1313 import FieldWindingSpecificationBase
    from mastapy._private.electric_machines._1314 import FillFactorSpecificationMethod
    from mastapy._private.electric_machines._1315 import FluxBarriers
    from mastapy._private.electric_machines._1316 import FluxBarrierOrWeb
    from mastapy._private.electric_machines._1317 import FluxBarrierStyle
    from mastapy._private.electric_machines._1318 import HairpinConductor
    from mastapy._private.electric_machines._1319 import (
        HarmonicLoadDataControlExcitationOptionForElectricMachineMode,
    )
    from mastapy._private.electric_machines._1320 import (
        IndividualConductorSpecificationSource,
    )
    from mastapy._private.electric_machines._1321 import (
        InteriorPermanentMagnetAndSynchronousReluctanceRotor,
    )
    from mastapy._private.electric_machines._1322 import InteriorPermanentMagnetMachine
    from mastapy._private.electric_machines._1323 import (
        IronLossCoefficientSpecificationMethod,
    )
    from mastapy._private.electric_machines._1324 import MagnetClearance
    from mastapy._private.electric_machines._1325 import MagnetConfiguration
    from mastapy._private.electric_machines._1326 import MagnetData
    from mastapy._private.electric_machines._1327 import MagnetDesign
    from mastapy._private.electric_machines._1328 import MagnetForLayer
    from mastapy._private.electric_machines._1329 import MagnetisationDirection
    from mastapy._private.electric_machines._1330 import MagnetMaterial
    from mastapy._private.electric_machines._1331 import MagnetMaterialDatabase
    from mastapy._private.electric_machines._1332 import MotorRotorSideFaceDetail
    from mastapy._private.electric_machines._1333 import NonCADElectricMachineDetail
    from mastapy._private.electric_machines._1334 import NotchShape
    from mastapy._private.electric_machines._1335 import NotchSpecification
    from mastapy._private.electric_machines._1336 import (
        PermanentMagnetAssistedSynchronousReluctanceMachine,
    )
    from mastapy._private.electric_machines._1337 import PermanentMagnetRotor
    from mastapy._private.electric_machines._1338 import Phase
    from mastapy._private.electric_machines._1339 import RegionID
    from mastapy._private.electric_machines._1340 import Rotor
    from mastapy._private.electric_machines._1341 import RotorInternalLayerSpecification
    from mastapy._private.electric_machines._1342 import RotorSkewSlice
    from mastapy._private.electric_machines._1343 import RotorType
    from mastapy._private.electric_machines._1344 import SingleOrDoubleLayerWindings
    from mastapy._private.electric_machines._1345 import SlotSectionDetail
    from mastapy._private.electric_machines._1346 import Stator
    from mastapy._private.electric_machines._1347 import StatorCutoutSpecification
    from mastapy._private.electric_machines._1348 import StatorRotorMaterial
    from mastapy._private.electric_machines._1349 import StatorRotorMaterialDatabase
    from mastapy._private.electric_machines._1350 import SurfacePermanentMagnetMachine
    from mastapy._private.electric_machines._1351 import SurfacePermanentMagnetRotor
    from mastapy._private.electric_machines._1352 import SynchronousReluctanceMachine
    from mastapy._private.electric_machines._1353 import ToothAndSlot
    from mastapy._private.electric_machines._1354 import ToothSlotStyle
    from mastapy._private.electric_machines._1355 import ToothTaperSpecification
    from mastapy._private.electric_machines._1356 import (
        TwoDimensionalFEModelForAnalysis,
    )
    from mastapy._private.electric_machines._1357 import (
        TwoDimensionalFEModelForElectromagneticAnalysis,
    )
    from mastapy._private.electric_machines._1358 import (
        TwoDimensionalFEModelForMechanicalAnalysis,
    )
    from mastapy._private.electric_machines._1359 import UShapedLayerSpecification
    from mastapy._private.electric_machines._1360 import VShapedMagnetLayerSpecification
    from mastapy._private.electric_machines._1361 import WindingConductor
    from mastapy._private.electric_machines._1362 import WindingConnection
    from mastapy._private.electric_machines._1363 import WindingMaterial
    from mastapy._private.electric_machines._1364 import WindingMaterialDatabase
    from mastapy._private.electric_machines._1365 import Windings
    from mastapy._private.electric_machines._1366 import WindingsViewer
    from mastapy._private.electric_machines._1367 import WindingType
    from mastapy._private.electric_machines._1368 import WireSizeSpecificationMethod
    from mastapy._private.electric_machines._1369 import WoundFieldSynchronousMachine
    from mastapy._private.electric_machines._1370 import WoundFieldSynchronousRotor
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines._1284": ["AbstractStator"],
        "_private.electric_machines._1285": ["AbstractToothAndSlot"],
        "_private.electric_machines._1286": ["CADConductor"],
        "_private.electric_machines._1287": ["CADElectricMachineDetail"],
        "_private.electric_machines._1288": ["CADFieldWindingSpecification"],
        "_private.electric_machines._1289": ["CADMagnetDetails"],
        "_private.electric_machines._1290": ["CADMagnetsForLayer"],
        "_private.electric_machines._1291": ["CADRotor"],
        "_private.electric_machines._1292": ["CADStator"],
        "_private.electric_machines._1293": ["CADToothAndSlot"],
        "_private.electric_machines._1294": ["CADWoundFieldSynchronousRotor"],
        "_private.electric_machines._1295": ["Coil"],
        "_private.electric_machines._1296": ["CoilPositionInSlot"],
        "_private.electric_machines._1297": ["CoolingDuctLayerSpecification"],
        "_private.electric_machines._1298": ["CoolingDuctShape"],
        "_private.electric_machines._1299": ["CoreLossBuildFactorSpecificationMethod"],
        "_private.electric_machines._1300": ["CoreLossCoefficients"],
        "_private.electric_machines._1301": ["DoubleLayerWindingSlotPositions"],
        "_private.electric_machines._1302": ["DQAxisConvention"],
        "_private.electric_machines._1303": ["Eccentricity"],
        "_private.electric_machines._1304": ["ElectricMachineDetail"],
        "_private.electric_machines._1305": ["ElectricMachineDetailInitialInformation"],
        "_private.electric_machines._1306": ["ElectricMachineGroup"],
        "_private.electric_machines._1307": [
            "ElectricMachineMechanicalAnalysisMeshingOptions"
        ],
        "_private.electric_machines._1308": ["ElectricMachineMeshingOptions"],
        "_private.electric_machines._1309": ["ElectricMachineMeshingOptionsBase"],
        "_private.electric_machines._1310": ["ElectricMachineSetup"],
        "_private.electric_machines._1311": ["ElectricMachineType"],
        "_private.electric_machines._1312": ["FieldWindingSpecification"],
        "_private.electric_machines._1313": ["FieldWindingSpecificationBase"],
        "_private.electric_machines._1314": ["FillFactorSpecificationMethod"],
        "_private.electric_machines._1315": ["FluxBarriers"],
        "_private.electric_machines._1316": ["FluxBarrierOrWeb"],
        "_private.electric_machines._1317": ["FluxBarrierStyle"],
        "_private.electric_machines._1318": ["HairpinConductor"],
        "_private.electric_machines._1319": [
            "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
        ],
        "_private.electric_machines._1320": ["IndividualConductorSpecificationSource"],
        "_private.electric_machines._1321": [
            "InteriorPermanentMagnetAndSynchronousReluctanceRotor"
        ],
        "_private.electric_machines._1322": ["InteriorPermanentMagnetMachine"],
        "_private.electric_machines._1323": ["IronLossCoefficientSpecificationMethod"],
        "_private.electric_machines._1324": ["MagnetClearance"],
        "_private.electric_machines._1325": ["MagnetConfiguration"],
        "_private.electric_machines._1326": ["MagnetData"],
        "_private.electric_machines._1327": ["MagnetDesign"],
        "_private.electric_machines._1328": ["MagnetForLayer"],
        "_private.electric_machines._1329": ["MagnetisationDirection"],
        "_private.electric_machines._1330": ["MagnetMaterial"],
        "_private.electric_machines._1331": ["MagnetMaterialDatabase"],
        "_private.electric_machines._1332": ["MotorRotorSideFaceDetail"],
        "_private.electric_machines._1333": ["NonCADElectricMachineDetail"],
        "_private.electric_machines._1334": ["NotchShape"],
        "_private.electric_machines._1335": ["NotchSpecification"],
        "_private.electric_machines._1336": [
            "PermanentMagnetAssistedSynchronousReluctanceMachine"
        ],
        "_private.electric_machines._1337": ["PermanentMagnetRotor"],
        "_private.electric_machines._1338": ["Phase"],
        "_private.electric_machines._1339": ["RegionID"],
        "_private.electric_machines._1340": ["Rotor"],
        "_private.electric_machines._1341": ["RotorInternalLayerSpecification"],
        "_private.electric_machines._1342": ["RotorSkewSlice"],
        "_private.electric_machines._1343": ["RotorType"],
        "_private.electric_machines._1344": ["SingleOrDoubleLayerWindings"],
        "_private.electric_machines._1345": ["SlotSectionDetail"],
        "_private.electric_machines._1346": ["Stator"],
        "_private.electric_machines._1347": ["StatorCutoutSpecification"],
        "_private.electric_machines._1348": ["StatorRotorMaterial"],
        "_private.electric_machines._1349": ["StatorRotorMaterialDatabase"],
        "_private.electric_machines._1350": ["SurfacePermanentMagnetMachine"],
        "_private.electric_machines._1351": ["SurfacePermanentMagnetRotor"],
        "_private.electric_machines._1352": ["SynchronousReluctanceMachine"],
        "_private.electric_machines._1353": ["ToothAndSlot"],
        "_private.electric_machines._1354": ["ToothSlotStyle"],
        "_private.electric_machines._1355": ["ToothTaperSpecification"],
        "_private.electric_machines._1356": ["TwoDimensionalFEModelForAnalysis"],
        "_private.electric_machines._1357": [
            "TwoDimensionalFEModelForElectromagneticAnalysis"
        ],
        "_private.electric_machines._1358": [
            "TwoDimensionalFEModelForMechanicalAnalysis"
        ],
        "_private.electric_machines._1359": ["UShapedLayerSpecification"],
        "_private.electric_machines._1360": ["VShapedMagnetLayerSpecification"],
        "_private.electric_machines._1361": ["WindingConductor"],
        "_private.electric_machines._1362": ["WindingConnection"],
        "_private.electric_machines._1363": ["WindingMaterial"],
        "_private.electric_machines._1364": ["WindingMaterialDatabase"],
        "_private.electric_machines._1365": ["Windings"],
        "_private.electric_machines._1366": ["WindingsViewer"],
        "_private.electric_machines._1367": ["WindingType"],
        "_private.electric_machines._1368": ["WireSizeSpecificationMethod"],
        "_private.electric_machines._1369": ["WoundFieldSynchronousMachine"],
        "_private.electric_machines._1370": ["WoundFieldSynchronousRotor"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADFieldWindingSpecification",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "CADWoundFieldSynchronousRotor",
    "Coil",
    "CoilPositionInSlot",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineGroup",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineType",
    "FieldWindingSpecification",
    "FieldWindingSpecificationBase",
    "FillFactorSpecificationMethod",
    "FluxBarriers",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutoutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "TwoDimensionalFEModelForElectromagneticAnalysis",
    "TwoDimensionalFEModelForMechanicalAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
    "WoundFieldSynchronousRotor",
)
