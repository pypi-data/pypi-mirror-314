from typing import Type, cast


def create_named_subclass[T](base_class: Type[T], subclass_suffix: str, prefix: str = "") -> Type[T]:
    """
    Creates a named subclass of a given base class.

    Args:
        base_class: The class to inherit from
        subclass_suffix: Name to convert into class name (e.g. 'my-name-1')
        prefix: Optional prefix for the class name

    Returns:
        A new subclass of base_class with formatted name

    Example:
        >>> MyClass = create_named_subclass(BaseClass, "my-name-1", "Custom")
        # Creates class CustomMyName1(BaseClass)
    """
    # Convert subclass-name---1 to SubclassName1
    class_name_parts = subclass_suffix.replace('_', '-').split('-')
    class_name_parts = [part for part in class_name_parts if part]  # Remove empty parts from double separators
    class_name = ''.join(part.capitalize() for part in class_name_parts)

    full_class_name = f"{prefix or base_class.__name__}{class_name}"

    return cast(Type[T], type(
        full_class_name,
        (base_class,),
        {
            '__doc__': f'{base_class.__name__} subclass for "{subclass_suffix}"',
            '_subclass_suffix': subclass_suffix
        }
    ))
