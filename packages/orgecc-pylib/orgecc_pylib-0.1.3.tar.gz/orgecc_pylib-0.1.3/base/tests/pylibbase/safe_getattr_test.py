import pytest

from base.pylibbase import safe_getattr


class HelperObject:
    def __init__(self):
        self.a = 'hello'
        self.b = HelperNestedObject()


class HelperNestedObject:
    def __init__(self):
        self.c = 'world'
        self.d = None


@pytest.fixture
def helper_obj():
    return HelperObject()


def test_valid_nested_attribute(helper_obj):
    assert safe_getattr(helper_obj, 'b', 'c') == 'world'


def test_missing_nested_attribute(helper_obj):
    assert safe_getattr(helper_obj, 'b', 'x') is None


def test_none_nested_object(helper_obj):
    assert safe_getattr(helper_obj, 'b', 'd') is None


def test_top_level_attribute(helper_obj):
    assert safe_getattr(helper_obj, 'a') == 'hello'


def test_missing_top_level_attribute(helper_obj):
    assert safe_getattr(helper_obj, 'x') is None


def test_missing_top_level_attribute_with_further_attributes(helper_obj):
    assert safe_getattr(helper_obj, 'x', 'y', 'z') is None


def test_none_object():
    assert safe_getattr(None, 'a') is None


def test_empty_attributes(helper_obj):
    assert safe_getattr(helper_obj) == helper_obj
