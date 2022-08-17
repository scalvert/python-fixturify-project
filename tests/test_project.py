"""Tests for Project class."""
from os import path
from pathlib import Path

import pytest
from conftest import BAD_DIR_NAME, BAD_EMPTY_NAME, GOOD_NESTED_DIRS, GOOD_SINGLE_FILE

from python_fixturify_project.exceptions import InvalidProjectError
from python_fixturify_project.project import Project


def test_project():
    """Example test with parametrization."""
    project = Project()
    assert isinstance(project, Project)


def test_cleanup_dir():
    # Given
    project = Project()
    project.write(GOOD_SINGLE_FILE)
    base_dir = project.base_dir

    assert path.exists(base_dir) and path.isdir(base_dir)

    # When
    del project

    # Then
    assert not path.exists(base_dir)


@pytest.mark.parametrize("test_input", [BAD_DIR_NAME, BAD_EMPTY_NAME])
def test_improper_write(test_input):
    with pytest.raises(InvalidProjectError):
        project = Project()
        project.write(test_input)


def test_proper_write_with_cleanup():
    base_dir = None

    with Project() as p:
        p.write(GOOD_NESTED_DIRS)
        base_dir = p.base_dir

        assert path.exists(base_dir) and path.isdir(base_dir)

        # Do some spot checking on the file structure
        file_checks = [
            (Path(base_dir, "valid_file.txt"), "file", "some text"),
            (Path(base_dir, "nested_dir"), "dir", None),
            (Path(base_dir, "nested_dir", "valid_empty_file"), "file", ""),
            (
                Path(
                    base_dir,
                    "nested_dir",
                    "another_nested_dir",
                    "last_nested_empty_dir",
                ),
                "dir",
                None,
            ),
            (
                Path(base_dir, "nested_dir", "another_nested_dir", "final_text_file"),
                "file",
                "some text",
            ),
        ]

        for file_path, file_type, file_contents in file_checks:
            if file_type == "file":
                assert path.exists(file_path) and path.isfile(file_path)
                with open(file_path) as _temp_file:
                    assert _temp_file.read() == file_contents
            else:
                assert path.exists(file_path) and path.isdir(file_path)

    # Ensure cleanup happened
    assert not path.exists(base_dir)
