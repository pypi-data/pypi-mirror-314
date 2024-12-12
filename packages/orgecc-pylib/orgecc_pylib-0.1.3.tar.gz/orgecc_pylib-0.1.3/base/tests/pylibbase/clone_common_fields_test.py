import pytest
from pydantic import BaseModel, ValidationError, Field

from base.pylibbase import clone_common_fields


# Define a sample source class and target Pydantic BaseModel
class SourceClassWith4Fields(BaseModel):
    field_one: str = Field("value_one", alias='field-one')
    field_two: str = Field("value_two", alias='field-two')
    field3: int = 3
    field_src_only: str = 4


class TargetModelOneMissing(BaseModel):
    field_one: str = Field(..., alias='field-one')
    field_two: str = Field(..., alias='field-two')
    field3: int = 0
    field_target_only: str = '*'


class SimpleBaseModelWithAlias(BaseModel):
    field_one: str = Field("value-one", alias='field-one')


class SimpleBaseModelNoAlias(BaseModel):
    field_one: str = Field("value_one")


def test_clone_common_fields_with_alias_from_dict():
    cloned_dict = clone_common_fields({'field-one': 'test-1'}, SimpleBaseModelWithAlias)
    assert cloned_dict == {'field-one': 'test-1'}
    assert SimpleBaseModelWithAlias(**cloned_dict).model_dump(by_alias=True) == cloned_dict


def test_clone_common_fields_with_alias_from_instance():
    expected = {'field-one': 'test-1'}
    cloned_dict = clone_common_fields(SimpleBaseModelWithAlias(**expected), SimpleBaseModelWithAlias)
    assert cloned_dict == expected
    assert SimpleBaseModelWithAlias(**cloned_dict).model_dump(by_alias=True) == cloned_dict


# Test basic functionality
def test_clone_common_fields_missing_src_and_target_fields():
    source = SourceClassWith4Fields()
    cloned_dict = clone_common_fields(source, TargetModelOneMissing)
    assert cloned_dict == {'field-one': source.field_one, 'field-two': source.field_two, 'field3': source.field3}
    assert TargetModelOneMissing(**cloned_dict).model_dump(by_alias=True) == cloned_dict | {'field_target_only': '*'}


# Test with no key transformer
def test_clone_common_fields_no_key_transformer():
    source = SourceClassWith4Fields()
    cloned_dict = clone_common_fields(source, TargetModelOneMissing, target2src_key_transformer=None)
    assert cloned_dict == {'field-one': source.field_one, 'field-two': source.field_two, 'field3': source.field3}


# Test skip fields functionality
def test_clone_common_fields_skip_fields():
    source = SourceClassWith4Fields()
    cloned_dict = clone_common_fields(source, TargetModelOneMissing, skip_fields={'field-one'})
    assert cloned_dict == {'field-two': source.field_two, 'field3': source.field3}
    with pytest.raises(ValidationError):
        TargetModelOneMissing(**cloned_dict)


# Test key transformer functionality
def test_clone_common_fields_key_transformer():
    source = SimpleBaseModelNoAlias()
    expected = {'FIELD_ONE': source.field_one}
    cloned_dict = clone_common_fields(expected, SimpleBaseModelNoAlias, target2src_key_transformer=lambda key: key.upper())
    assert cloned_dict == {k.lower(): expected[k] for k in expected}


# Test edge case: No common fields
def test_clone_common_fields_no_common_fields():
    class DifferentModel(BaseModel):
        different_field: str

    assert clone_common_fields(SourceClassWith4Fields(), DifferentModel) == {}


# Test with non-existent fields in the skip list
def test_clone_with_nonexistent_skip_fields():
    source = SourceClassWith4Fields()
    cloned = clone_common_fields(source, TargetModelOneMissing, skip_fields={'nonexistent_field'})
    assert cloned == {'field-one': source.field_one, 'field-two': source.field_two, 'field3': source.field3}


# Test with an invalid key transformer
def test_clone_with_invalid_key_transformer():
    source = SourceClassWith4Fields()
    with pytest.raises(ValidationError):
        TargetModelOneMissing(**clone_common_fields(source, TargetModelOneMissing, target2src_key_transformer=(lambda key: 'invalid key')))


# Test for type mismatch between source and target
def test_clone_with_type_mismatch():
    class SourceClassMismatch:
        field_one = 123  # Intentional type mismatch (int instead of str)

    source = SourceClassMismatch()
    with pytest.raises(ValidationError):
        target = TargetModelOneMissing(**clone_common_fields(source, TargetModelOneMissing))
        print(f'Failed. Target: {target}')
