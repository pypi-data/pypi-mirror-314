import pytest
from pathlib import Path
from pylibtypes.folder_based_class_attrs import load_class_attrs_from_folder, FolderBasedAttrsError


@pytest.fixture
def temp_folder(tmp_path):
    # Create a temporary folder with test files
    folder = tmp_path / "test_folder"
    folder.mkdir()

    # Create valid text file
    text_file = folder / "sample_text.txt"
    text_file.write_text("Hello World", encoding='utf-8')

    # Create valid cedarml file
    cedarml_file = folder / "sample_cedarml.cedarml"
    cedarml_file.write_text("[key: value]", encoding='utf-8')

    # Create empty file (invalid)
    empty_file = folder / "empty.txt"
    empty_file.write_text("", encoding='utf-8')

    # Create hidden file
    hidden_file = folder / ".hidden.txt"
    hidden_file.write_text("hidden content", encoding='utf-8')

    return folder


def mock_cedarml_parser(content: str) -> list[dict[str, str]]:
    # Simple mock parser that returns a list with one dict
    return [{"key": "value"}]


class TestFolderBasedClassAttrs:

    @pytest.mark.skip(reason="Check later")
    def test_valid_loading(self, temp_folder):
        class TestClass:
            pass

        target = TestClass()
        load_class_attrs_from_folder(temp_folder, target, mock_cedarml_parser)

        assert hasattr(target, "sample_text")
        assert target.sample_text == "Hello World"
        assert hasattr(target, "sample_cedarml")
        assert target.sample_cedarml == [{"key": "value"}]

    def test_nonexistent_folder(self):
        class TestClass:
            pass

        with pytest.raises(FileNotFoundError, match=".*nonexistent_folder.*"):
            load_class_attrs_from_folder("nonexistent_folder", TestClass(), mock_cedarml_parser)

    def test_empty_folder(self, temp_folder):
        # Remove all files from temp folder
        for file in temp_folder.iterdir():
            file.unlink()

        class TestClass:
            pass

        with pytest.raises(FolderBasedAttrsError, match="No valid files found"):
            load_class_attrs_from_folder(temp_folder, TestClass(), mock_cedarml_parser)

    def test_none_folder(self):
        class TestClass:
            pass

        with pytest.raises(FolderBasedAttrsError, match="Folder name must be a non-empty string"):
            load_class_attrs_from_folder(None, TestClass(), mock_cedarml_parser)

    @pytest.mark.skip(reason="Check later")
    def test_invalid_content(self, temp_folder):
        # Create file with empty content
        empty_file = temp_folder / "empty_content.txt"
        empty_file.write_text("", encoding='utf-8')

        class TestClass:
            pass

        with pytest.raises(FolderBasedAttrsError, match="No valid files found in"):
            load_class_attrs_from_folder(temp_folder, TestClass(), mock_cedarml_parser)

    def test_hidden_files_ignored(self, temp_folder):
        # Remove all regular files, leaving only hidden
        for file in temp_folder.iterdir():
            if not file.name.startswith('.'):
                file.unlink()

        class TestClass:
            pass

        with pytest.raises(FolderBasedAttrsError, match="No valid files found"):
            load_class_attrs_from_folder(temp_folder, TestClass(), mock_cedarml_parser)

    @pytest.mark.skip(reason="Check later")
    def test_path_object_input(self, temp_folder):
        class TestClass:
            pass

        target = TestClass()
        load_class_attrs_from_folder(Path(temp_folder), target, mock_cedarml_parser)

        assert hasattr(target, "sample_text")
        assert target.sample_text == "Hello World"
