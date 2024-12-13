"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.roller_bearing_profiles._1982 import ProfileDataToUse
    from mastapy._private.bearings.roller_bearing_profiles._1983 import ProfileSet
    from mastapy._private.bearings.roller_bearing_profiles._1984 import ProfileToFit
    from mastapy._private.bearings.roller_bearing_profiles._1985 import (
        RollerBearingConicalProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1986 import (
        RollerBearingCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1987 import (
        RollerBearingDinLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1988 import (
        RollerBearingFlatProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1989 import (
        RollerBearingJohnsGoharProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1990 import (
        RollerBearingLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1991 import (
        RollerBearingProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1992 import (
        RollerBearingTangentialCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1993 import (
        RollerBearingUserSpecifiedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1994 import (
        RollerRaceProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1995 import (
        UserSpecifiedProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._1996 import (
        UserSpecifiedRollerRaceProfilePoint,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.roller_bearing_profiles._1982": ["ProfileDataToUse"],
        "_private.bearings.roller_bearing_profiles._1983": ["ProfileSet"],
        "_private.bearings.roller_bearing_profiles._1984": ["ProfileToFit"],
        "_private.bearings.roller_bearing_profiles._1985": [
            "RollerBearingConicalProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1986": [
            "RollerBearingCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1987": [
            "RollerBearingDinLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1988": ["RollerBearingFlatProfile"],
        "_private.bearings.roller_bearing_profiles._1989": [
            "RollerBearingJohnsGoharProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1990": [
            "RollerBearingLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1991": ["RollerBearingProfile"],
        "_private.bearings.roller_bearing_profiles._1992": [
            "RollerBearingTangentialCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1993": [
            "RollerBearingUserSpecifiedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._1994": ["RollerRaceProfilePoint"],
        "_private.bearings.roller_bearing_profiles._1995": [
            "UserSpecifiedProfilePoint"
        ],
        "_private.bearings.roller_bearing_profiles._1996": [
            "UserSpecifiedRollerRaceProfilePoint"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ProfileDataToUse",
    "ProfileSet",
    "ProfileToFit",
    "RollerBearingConicalProfile",
    "RollerBearingCrownedProfile",
    "RollerBearingDinLundbergProfile",
    "RollerBearingFlatProfile",
    "RollerBearingJohnsGoharProfile",
    "RollerBearingLundbergProfile",
    "RollerBearingProfile",
    "RollerBearingTangentialCrownedProfile",
    "RollerBearingUserSpecifiedProfile",
    "RollerRaceProfilePoint",
    "UserSpecifiedProfilePoint",
    "UserSpecifiedRollerRaceProfilePoint",
)
