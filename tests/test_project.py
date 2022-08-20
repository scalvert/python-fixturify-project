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


def test_proper_write_with_cleanup(snapshot):
    base_dir = None

    with Project(files=GOOD_NESTED_DIRS) as p:
        base_dir = p.base_dir

        assert path.exists(base_dir) and path.isdir(base_dir)

        assert p.read() == snapshot

    # Ensure cleanup happened
    assert not path.exists(base_dir)


def test_read(snapshot):
    with Project(files=GOOD_NESTED_DIRS) as p:

        dir_json = p.read()

        assert dir_json == snapshot
