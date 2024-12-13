"""ConicalMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _379

_CONICAL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.bevel.standards import _571, _573, _575
    from mastapy._private.gears.rating.hypoid.standards import _456
    from mastapy._private.gears.rating.iso_10300 import _435, _436, _437, _438, _439

    Self = TypeVar("Self", bound="ConicalMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshSingleFlankRating._Cast_ConicalMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshSingleFlankRating:
    """Special nested class for casting ConicalMeshSingleFlankRating to subclasses."""

    __parent__: "ConicalMeshSingleFlankRating"

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_379.MeshSingleFlankRating":
        return self.__parent__._cast(_379.MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_435.ISO10300MeshSingleFlankRating":
        from mastapy._private.gears.rating.iso_10300 import _435

        return self.__parent__._cast(_435.ISO10300MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_436.ISO10300MeshSingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _436

        return self.__parent__._cast(_436.ISO10300MeshSingleFlankRatingBevelMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_437.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _437

        return self.__parent__._cast(_437.ISO10300MeshSingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_438.ISO10300MeshSingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _438

        return self.__parent__._cast(_438.ISO10300MeshSingleFlankRatingMethodB1)

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_439.ISO10300MeshSingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _439

        return self.__parent__._cast(_439.ISO10300MeshSingleFlankRatingMethodB2)

    @property
    def gleason_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_456.GleasonHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.hypoid.standards import _456

        return self.__parent__._cast(_456.GleasonHypoidMeshSingleFlankRating)

    @property
    def agma_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_571.AGMASpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _571

        return self.__parent__._cast(_571.AGMASpiralBevelMeshSingleFlankRating)

    @property
    def gleason_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_573.GleasonSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _573

        return self.__parent__._cast(_573.GleasonSpiralBevelMeshSingleFlankRating)

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_575.SpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _575

        return self.__parent__._cast(_575.SpiralBevelMeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ConicalMeshSingleFlankRating":
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
class ConicalMeshSingleFlankRating(_379.MeshSingleFlankRating):
    """ConicalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshSingleFlankRating
        """
        return _Cast_ConicalMeshSingleFlankRating(self)
