"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2678 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2679 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2680 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2681 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2682 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2683 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2684 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2685 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2678": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2679": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2680": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2681": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2682": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2683": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2684": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2685": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
