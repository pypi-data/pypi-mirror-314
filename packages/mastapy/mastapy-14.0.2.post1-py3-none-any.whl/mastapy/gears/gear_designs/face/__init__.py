"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.face._1015 import FaceGearDesign
    from mastapy._private.gears.gear_designs.face._1016 import (
        FaceGearDiameterFaceWidthSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.face._1017 import FaceGearMeshDesign
    from mastapy._private.gears.gear_designs.face._1018 import FaceGearMeshMicroGeometry
    from mastapy._private.gears.gear_designs.face._1019 import FaceGearMicroGeometry
    from mastapy._private.gears.gear_designs.face._1020 import FaceGearPinionDesign
    from mastapy._private.gears.gear_designs.face._1021 import FaceGearSetDesign
    from mastapy._private.gears.gear_designs.face._1022 import FaceGearSetMicroGeometry
    from mastapy._private.gears.gear_designs.face._1023 import FaceGearWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.face._1015": ["FaceGearDesign"],
        "_private.gears.gear_designs.face._1016": [
            "FaceGearDiameterFaceWidthSpecificationMethod"
        ],
        "_private.gears.gear_designs.face._1017": ["FaceGearMeshDesign"],
        "_private.gears.gear_designs.face._1018": ["FaceGearMeshMicroGeometry"],
        "_private.gears.gear_designs.face._1019": ["FaceGearMicroGeometry"],
        "_private.gears.gear_designs.face._1020": ["FaceGearPinionDesign"],
        "_private.gears.gear_designs.face._1021": ["FaceGearSetDesign"],
        "_private.gears.gear_designs.face._1022": ["FaceGearSetMicroGeometry"],
        "_private.gears.gear_designs.face._1023": ["FaceGearWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDesign",
    "FaceGearDiameterFaceWidthSpecificationMethod",
    "FaceGearMeshDesign",
    "FaceGearMeshMicroGeometry",
    "FaceGearMicroGeometry",
    "FaceGearPinionDesign",
    "FaceGearSetDesign",
    "FaceGearSetMicroGeometry",
    "FaceGearWheelDesign",
)
