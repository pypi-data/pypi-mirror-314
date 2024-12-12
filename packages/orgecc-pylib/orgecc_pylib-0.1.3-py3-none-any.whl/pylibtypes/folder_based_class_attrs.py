import re
from pathlib import Path
from typing import Callable
from importlib.resources.abc import Traversable


class FolderBasedAttrsError(Exception):
    """Custom exception for folder-related errors"""
    pass


def load_class_attrs_from_folder[T](
        folder: str | Path | Traversable, target: T,
        cedarml_parser: Callable[[str], list[dict[str, str]]] | None = None
) -> None:
    match folder:
        case None:
            raise FolderBasedAttrsError("Folder name must be a non-empty string")
        case str():
            folder = Path(folder)

    loaded_files = False

    # Load all .txt and .xml files
    for file_path in folder.iterdir():
        if not file_path.is_file() or file_path.name.startswith('.'):
            continue

        attr_name, file_suffix = file_parts(file_path)
        if file_suffix not in ['txt', 'cedarml']:
            continue

        try:
            content = file_path.read_text(encoding='utf-8')

            if not _is_valid_content(content, file_path):
                raise FolderBasedAttrsError(
                    f"Invalid or empty content in file: {file_path}"
                )

            if file_suffix == 'cedarml' and cedarml_parser is not None:
                content = cedarml_parser(content)

            setattr(target, attr_name, content)
            loaded_files = True

        except (IOError, UnicodeDecodeError) as e:
            raise FolderBasedAttrsError(
                f"Error reading file {file_path}: {str(e)}"
            ) from e

    if not loaded_files:
        raise FolderBasedAttrsError(
            f"No valid files found in {folder}"
        )


def _is_valid_content(content: str, file_path: str | Path | Traversable) -> bool:
    """Basic content validation"""

    _, file_suffix = file_parts(file_path)
    if file_suffix == '.xml':
        # Check for basic XML-like structure
        return bool(re.search(r'<\w+>.*?</\w+>', content, re.DOTALL))

    return True

def file_parts(file: str | Path | Traversable) -> tuple[str, str]:
    file_name, *file_suffix = file.name.rsplit('.', 1)
    return file_name, (file_suffix[0] if file_suffix else '')
