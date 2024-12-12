"""
xmlapply - A tool for applying XML-defined file changes to a project directory
"""

from .parser import FileChange, parse_xml_string
from .apply import apply_file_changes, ChangeApplicationError
from .config import get_config, set_default_directory, get_default_directory

__version__ = "0.1.0"

__all__ = [
    "FileChange",
    "parse_xml_string",
    "apply_file_changes",
    "ChangeApplicationError",
    "get_config",
    "set_default_directory",
    "get_default_directory",
]
