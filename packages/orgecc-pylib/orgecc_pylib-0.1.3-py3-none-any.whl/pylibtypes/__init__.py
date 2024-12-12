"""Miscellaneous functions
"""
from version import __version__
__author__ = 'Elifarley'

from .named_subclass_factory import create_named_subclass
from .folder_based_class_attrs import load_class_attrs_from_folder, FolderBasedAttrsError
