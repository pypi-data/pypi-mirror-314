"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2191 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2192 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2193 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2194 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2195 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2196 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2197 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2198 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2199 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2200 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2201 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2202 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2203 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2204 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2205 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2206 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2207 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2208 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2209 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2210 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2211 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2212 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2213 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2214 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2215 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2216 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2217 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2218 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2219 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2220 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2221 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2222 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2223 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2224 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2225 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2226 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2227 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2228 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2229 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2230 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2231 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2232 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2191": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2192": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2193": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2194": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2195": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2196": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2197": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2198": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2199": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2200": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2201": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2202": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2203": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2204": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2205": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2206": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2207": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2208": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2209": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2210": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2211": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2212": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2213": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2214": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2215": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2216": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2217": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2218": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2219": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2220": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2221": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2222": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2223": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2224": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2225": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2226": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2227": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2228": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2229": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2230": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2231": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2232": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
