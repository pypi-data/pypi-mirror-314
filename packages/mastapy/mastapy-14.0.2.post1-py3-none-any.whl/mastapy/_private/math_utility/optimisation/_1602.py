"""ParetoOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1590

_PARETO_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationStrategyDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _949,
        _950,
        _951,
        _952,
        _953,
        _954,
        _955,
        _956,
        _957,
        _959,
        _960,
        _961,
        _962,
    )
    from mastapy._private.utility.databases import _1879, _1883, _1886

    Self = TypeVar("Self", bound="ParetoOptimisationStrategyDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoOptimisationStrategyDatabase._Cast_ParetoOptimisationStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationStrategyDatabase:
    """Special nested class for casting ParetoOptimisationStrategyDatabase to subclasses."""

    __parent__: "ParetoOptimisationStrategyDatabase"

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1590.DesignSpaceSearchStrategyDatabase":
        return self.__parent__._cast(_1590.DesignSpaceSearchStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1883.NamedDatabase":
        pass

        from mastapy._private.utility.databases import _1883

        return self.__parent__._cast(_1883.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1886.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1886

        return self.__parent__._cast(_1886.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1879.Database":
        pass

        from mastapy._private.utility.databases import _1879

        return self.__parent__._cast(_1879.Database)

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_949.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _949

        return self.__parent__._cast(
            _949.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_950.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _950

        return self.__parent__._cast(
            _950.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_951.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _951

        return self.__parent__._cast(
            _951.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_952.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _952

        return self.__parent__._cast(
            _952.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_953.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _953

        return self.__parent__._cast(
            _953.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_954.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _954

        return self.__parent__._cast(_954.ParetoFaceGearSetOptimisationStrategyDatabase)

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_955.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _955

        return self.__parent__._cast(_955.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _956

        return self.__parent__._cast(
            _956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_957.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _957

        return self.__parent__._cast(
            _957.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _959

        return self.__parent__._cast(
            _959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _960

        return self.__parent__._cast(
            _960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _961

        return self.__parent__._cast(
            _961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_962.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _962

        return self.__parent__._cast(
            _962.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "ParetoOptimisationStrategyDatabase":
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
class ParetoOptimisationStrategyDatabase(_1590.DesignSpaceSearchStrategyDatabase):
    """ParetoOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_STRATEGY_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationStrategyDatabase
        """
        return _Cast_ParetoOptimisationStrategyDatabase(self)
