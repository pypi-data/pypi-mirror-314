from dataclasses import dataclass
from typing import ClassVar

from pylibtypes.named_subclass_factory import create_named_subclass


@dataclass
class BaseTestClass:
    name: str
    STATIC_VALUE: ClassVar[str] = "base"


def test_create_named_subclass_basic():
    # Test basic subclass creation
    SubClass = create_named_subclass(BaseTestClass, "test-name-1")

    # Verify class name
    assert SubClass.__name__ == "BaseTestClassTestName1"

    # Verify inheritance
    assert issubclass(SubClass, BaseTestClass)

    # Verify instance creation and inheritance
    instance = SubClass(name="test")
    assert isinstance(instance, BaseTestClass)
    assert instance.name == "test"
    assert instance.STATIC_VALUE == "base"

    # Verify instance name storage
    assert getattr(SubClass, '_subclass_suffix') == "test-name-1"


def test_create_named_subclass_with_prefix():
    # Test subclass creation with prefix
    SubClass = create_named_subclass(BaseTestClass, "test-name-2", prefix="Custom")

    # Verify class name includes prefix
    assert SubClass.__name__ == "CustomTestName2"

    # Verify inheritance still works
    assert issubclass(SubClass, BaseTestClass)


def test_create_named_subclass_empty_name():
    # Test with empty instance name
    SubClass = create_named_subclass(BaseTestClass, "")
    assert SubClass.__name__ == "BaseTestClass"


def test_create_named_subclass_special_chars():
    # Test with various special characters and separators
    SubClass = create_named_subclass(BaseTestClass, "test--name__123")
    assert SubClass.__name__ == "BaseTestClassTestName123"


def test_create_named_subclass_docstring():
    SubClass = create_named_subclass(BaseTestClass, "test-name")
    assert SubClass.__doc__ == 'BaseTestClass subclass for "test-name"'
