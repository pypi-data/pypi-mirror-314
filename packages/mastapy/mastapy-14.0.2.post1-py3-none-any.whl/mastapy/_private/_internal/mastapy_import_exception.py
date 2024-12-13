"""mastapy_import_exception.

Module containing mastapy import exceptions.
"""

from __future__ import annotations


class MastapyImportException(Exception):
    """Custom exception for errors on import.

    We can't use the ImportError class because that just gets swallowed.
    """
