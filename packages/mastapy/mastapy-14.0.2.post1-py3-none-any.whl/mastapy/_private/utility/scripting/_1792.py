"""ScriptingSetup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1645

_SCRIPTING_SETUP = python_net_import("SMT.MastaAPI.Utility.Scripting", "ScriptingSetup")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1646

    Self = TypeVar("Self", bound="ScriptingSetup")
    CastSelf = TypeVar("CastSelf", bound="ScriptingSetup._Cast_ScriptingSetup")


__docformat__ = "restructuredtext en"
__all__ = ("ScriptingSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScriptingSetup:
    """Special nested class for casting ScriptingSetup to subclasses."""

    __parent__: "ScriptingSetup"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1645.PerMachineSettings":
        return self.__parent__._cast(_1645.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1646.PersistentSingleton":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PersistentSingleton)

    @property
    def scripting_setup(self: "CastSelf") -> "ScriptingSetup":
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
class ScriptingSetup(_1645.PerMachineSettings):
    """ScriptingSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCRIPTING_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def display_python_property_hints(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DisplayPythonPropertyHints")

        if temp is None:
            return False

        return temp

    @display_python_property_hints.setter
    @enforce_parameter_types
    def display_python_property_hints(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisplayPythonPropertyHints",
            bool(value) if value is not None else False,
        )

    @property
    def image_height(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ImageHeight")

        if temp is None:
            return 0

        return temp

    @image_height.setter
    @enforce_parameter_types
    def image_height(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ImageHeight", int(value) if value is not None else 0
        )

    @property
    def image_width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ImageWidth")

        if temp is None:
            return 0

        return temp

    @image_width.setter
    @enforce_parameter_types
    def image_width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ImageWidth", int(value) if value is not None else 0
        )

    @property
    def load_scripted_properties_when_opening_masta(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LoadScriptedPropertiesWhenOpeningMASTA"
        )

        if temp is None:
            return False

        return temp

    @load_scripted_properties_when_opening_masta.setter
    @enforce_parameter_types
    def load_scripted_properties_when_opening_masta(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadScriptedPropertiesWhenOpeningMASTA",
            bool(value) if value is not None else False,
        )

    @property
    def mastapy_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MastapyVersion")

        if temp is None:
            return ""

        return temp

    @property
    def python_exe_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PythonExePath")

        if temp is None:
            return ""

        return temp

    @property
    def python_home_directory(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PythonHomeDirectory")

        if temp is None:
            return ""

        return temp

    @property
    def python_install_directory(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "PythonInstallDirectory")

        if temp is None:
            return ""

        return temp

    @python_install_directory.setter
    @enforce_parameter_types
    def python_install_directory(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PythonInstallDirectory",
            str(value) if value is not None else "",
        )

    @property
    def python_remote_host(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "PythonRemoteHost")

        if temp is None:
            return ""

        return temp

    @python_remote_host.setter
    @enforce_parameter_types
    def python_remote_host(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "PythonRemoteHost", str(value) if value is not None else ""
        )

    @property
    def python_remote_port(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PythonRemotePort")

        if temp is None:
            return 0

        return temp

    @python_remote_port.setter
    @enforce_parameter_types
    def python_remote_port(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PythonRemotePort", int(value) if value is not None else 0
        )

    @property
    def python_remote_timeout_s(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PythonRemoteTimeoutS")

        if temp is None:
            return 0

        return temp

    @python_remote_timeout_s.setter
    @enforce_parameter_types
    def python_remote_timeout_s(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PythonRemoteTimeoutS", int(value) if value is not None else 0
        )

    @property
    def run_scripts_in_separate_threads(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RunScriptsInSeparateThreads")

        if temp is None:
            return False

        return temp

    @run_scripts_in_separate_threads.setter
    @enforce_parameter_types
    def run_scripts_in_separate_threads(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RunScriptsInSeparateThreads",
            bool(value) if value is not None else False,
        )

    @property
    def use_default_net_solution_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultNETSolutionDirectory")

        if temp is None:
            return False

        return temp

    @use_default_net_solution_directory.setter
    @enforce_parameter_types
    def use_default_net_solution_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultNETSolutionDirectory",
            bool(value) if value is not None else False,
        )

    @property
    def use_default_plugin_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultPluginDirectory")

        if temp is None:
            return False

        return temp

    @use_default_plugin_directory.setter
    @enforce_parameter_types
    def use_default_plugin_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultPluginDirectory",
            bool(value) if value is not None else False,
        )

    @property
    def use_default_python_scripts_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultPythonScriptsDirectory")

        if temp is None:
            return False

        return temp

    @use_default_python_scripts_directory.setter
    @enforce_parameter_types
    def use_default_python_scripts_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultPythonScriptsDirectory",
            bool(value) if value is not None else False,
        )

    @property
    def use_default_visual_studio_code_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseDefaultVisualStudioCodeDirectory"
        )

        if temp is None:
            return False

        return temp

    @use_default_visual_studio_code_directory.setter
    @enforce_parameter_types
    def use_default_visual_studio_code_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultVisualStudioCodeDirectory",
            bool(value) if value is not None else False,
        )

    @property
    def visual_studio_code_directory(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "VisualStudioCodeDirectory")

        if temp is None:
            return ""

        return temp

    @visual_studio_code_directory.setter
    @enforce_parameter_types
    def visual_studio_code_directory(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VisualStudioCodeDirectory",
            str(value) if value is not None else "",
        )

    def add_existing_net_solution(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddExistingNETSolution")

    def restore_api_packages(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RestoreAPIPackages")

    def select_net_solution_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectNETSolutionDirectory")

    def select_plugin_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectPluginDirectory")

    def select_python_install_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectPythonInstallDirectory")

    def select_python_scripts_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectPythonScriptsDirectory")

    def select_visual_studio_code_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectVisualStudioCodeDirectory")

    @property
    def cast_to(self: "Self") -> "_Cast_ScriptingSetup":
        """Cast to another type.

        Returns:
            _Cast_ScriptingSetup
        """
        return _Cast_ScriptingSetup(self)
