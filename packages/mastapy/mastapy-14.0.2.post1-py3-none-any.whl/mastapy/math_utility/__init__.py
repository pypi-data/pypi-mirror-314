"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility._1539 import Range
    from mastapy._private.math_utility._1540 import AcousticWeighting
    from mastapy._private.math_utility._1541 import AlignmentAxis
    from mastapy._private.math_utility._1542 import Axis
    from mastapy._private.math_utility._1543 import CirclesOnAxis
    from mastapy._private.math_utility._1544 import ComplexMatrix
    from mastapy._private.math_utility._1545 import ComplexPartDisplayOption
    from mastapy._private.math_utility._1546 import ComplexVector
    from mastapy._private.math_utility._1547 import ComplexVector3D
    from mastapy._private.math_utility._1548 import ComplexVector6D
    from mastapy._private.math_utility._1549 import CoordinateSystem3D
    from mastapy._private.math_utility._1550 import CoordinateSystemEditor
    from mastapy._private.math_utility._1551 import CoordinateSystemForRotation
    from mastapy._private.math_utility._1552 import CoordinateSystemForRotationOrigin
    from mastapy._private.math_utility._1553 import DataPrecision
    from mastapy._private.math_utility._1554 import DegreeOfFreedom
    from mastapy._private.math_utility._1555 import DynamicsResponseScalarResult
    from mastapy._private.math_utility._1556 import DynamicsResponseScaling
    from mastapy._private.math_utility._1557 import Eigenmode
    from mastapy._private.math_utility._1558 import Eigenmodes
    from mastapy._private.math_utility._1559 import EulerParameters
    from mastapy._private.math_utility._1560 import ExtrapolationOptions
    from mastapy._private.math_utility._1561 import FacetedBody
    from mastapy._private.math_utility._1562 import FacetedSurface
    from mastapy._private.math_utility._1563 import FourierSeries
    from mastapy._private.math_utility._1564 import GenericMatrix
    from mastapy._private.math_utility._1565 import GriddedSurface
    from mastapy._private.math_utility._1566 import HarmonicValue
    from mastapy._private.math_utility._1567 import InertiaTensor
    from mastapy._private.math_utility._1568 import MassProperties
    from mastapy._private.math_utility._1569 import MaxMinMean
    from mastapy._private.math_utility._1570 import ComplexMagnitudeMethod
    from mastapy._private.math_utility._1571 import MultipleFourierSeriesInterpolator
    from mastapy._private.math_utility._1572 import Named2DLocation
    from mastapy._private.math_utility._1573 import PIDControlUpdateMethod
    from mastapy._private.math_utility._1574 import Quaternion
    from mastapy._private.math_utility._1575 import RealMatrix
    from mastapy._private.math_utility._1576 import RealVector
    from mastapy._private.math_utility._1577 import ResultOptionsFor3DVector
    from mastapy._private.math_utility._1578 import RotationAxis
    from mastapy._private.math_utility._1579 import RoundedOrder
    from mastapy._private.math_utility._1580 import SinCurve
    from mastapy._private.math_utility._1581 import SquareMatrix
    from mastapy._private.math_utility._1582 import StressPoint
    from mastapy._private.math_utility._1583 import TransformMatrix3D
    from mastapy._private.math_utility._1584 import TranslationRotation
    from mastapy._private.math_utility._1585 import Vector2DListAccessor
    from mastapy._private.math_utility._1586 import Vector6D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility._1539": ["Range"],
        "_private.math_utility._1540": ["AcousticWeighting"],
        "_private.math_utility._1541": ["AlignmentAxis"],
        "_private.math_utility._1542": ["Axis"],
        "_private.math_utility._1543": ["CirclesOnAxis"],
        "_private.math_utility._1544": ["ComplexMatrix"],
        "_private.math_utility._1545": ["ComplexPartDisplayOption"],
        "_private.math_utility._1546": ["ComplexVector"],
        "_private.math_utility._1547": ["ComplexVector3D"],
        "_private.math_utility._1548": ["ComplexVector6D"],
        "_private.math_utility._1549": ["CoordinateSystem3D"],
        "_private.math_utility._1550": ["CoordinateSystemEditor"],
        "_private.math_utility._1551": ["CoordinateSystemForRotation"],
        "_private.math_utility._1552": ["CoordinateSystemForRotationOrigin"],
        "_private.math_utility._1553": ["DataPrecision"],
        "_private.math_utility._1554": ["DegreeOfFreedom"],
        "_private.math_utility._1555": ["DynamicsResponseScalarResult"],
        "_private.math_utility._1556": ["DynamicsResponseScaling"],
        "_private.math_utility._1557": ["Eigenmode"],
        "_private.math_utility._1558": ["Eigenmodes"],
        "_private.math_utility._1559": ["EulerParameters"],
        "_private.math_utility._1560": ["ExtrapolationOptions"],
        "_private.math_utility._1561": ["FacetedBody"],
        "_private.math_utility._1562": ["FacetedSurface"],
        "_private.math_utility._1563": ["FourierSeries"],
        "_private.math_utility._1564": ["GenericMatrix"],
        "_private.math_utility._1565": ["GriddedSurface"],
        "_private.math_utility._1566": ["HarmonicValue"],
        "_private.math_utility._1567": ["InertiaTensor"],
        "_private.math_utility._1568": ["MassProperties"],
        "_private.math_utility._1569": ["MaxMinMean"],
        "_private.math_utility._1570": ["ComplexMagnitudeMethod"],
        "_private.math_utility._1571": ["MultipleFourierSeriesInterpolator"],
        "_private.math_utility._1572": ["Named2DLocation"],
        "_private.math_utility._1573": ["PIDControlUpdateMethod"],
        "_private.math_utility._1574": ["Quaternion"],
        "_private.math_utility._1575": ["RealMatrix"],
        "_private.math_utility._1576": ["RealVector"],
        "_private.math_utility._1577": ["ResultOptionsFor3DVector"],
        "_private.math_utility._1578": ["RotationAxis"],
        "_private.math_utility._1579": ["RoundedOrder"],
        "_private.math_utility._1580": ["SinCurve"],
        "_private.math_utility._1581": ["SquareMatrix"],
        "_private.math_utility._1582": ["StressPoint"],
        "_private.math_utility._1583": ["TransformMatrix3D"],
        "_private.math_utility._1584": ["TranslationRotation"],
        "_private.math_utility._1585": ["Vector2DListAccessor"],
        "_private.math_utility._1586": ["Vector6D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Range",
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TransformMatrix3D",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
