from distutils.dir_util import copy_tree
from os import path
from pathlib import Path

import pytest
from conftest import BAD_DIR_NAME, BAD_EMPTY_NAME, GOOD_NESTED_DIRS, GOOD_SINGLE_FILE
from deepdiff import DeepDiff

from python_fixturify_project.exceptions import InvalidProjectError
from python_fixturify_project.project import Project


def test_project():
    """Example test with parametrization."""
    project = Project()
    assert isinstance(project, Project)


def test_project_has_base_dir_on_instantiation():
    project = Project()
    assert type(project.base_dir) is str


def test_cleanup_dir():
    project = Project()
    project.write(GOOD_SINGLE_FILE)
    base_dir = project.base_dir

    assert path.exists(base_dir) and path.isdir(base_dir)

    del project

    assert not path.exists(base_dir)


def test_get_files_after_copy(snapshot):
    project1 = Project(
        files={
            "one.py": "# some python",
            "dir": {
                "two.py": "# another python",
                "dir2": {"three.py": "# and this makes 3!!!"},
            },
        }
    )

    project2 = Project()

    copy_tree(project1.base_dir, project2.base_dir)

    assert project2.files == snapshot


def test_get_from_files(snapshot):
    project = Project(
        files={
            "one.py": "# some python",
            "dir": {
                "two.py": "# another python",
                "dir2": {"three.py": "# and this makes 3!!!"},
            },
        }
    )

    assert project.get("one.py") == snapshot(name="one.py")
    assert project.get("dir") == snapshot(name="dir")
    assert project.get("dir/dir2") == snapshot(name="dir2")


def test_get_from_copied_files(snapshot):
    project1 = Project(
        files={
            "one.py": "# some python",
            "dir": {
                "two.py": "# another python",
                "dir2": {"three.py": "# and this makes 3!!!"},
            },
        }
    )

    project2 = Project()

    copy_tree(project1.base_dir, project2.base_dir)

    project2.get("one.py")

    assert project2.files == snapshot
    assert DeepDiff(project1.files, project2.files) == {}


@pytest.mark.parametrize("test_input", [BAD_DIR_NAME, BAD_EMPTY_NAME])
def test_improper_write(test_input):
    with pytest.raises(InvalidProjectError):
        project = Project()
        project.write(test_input)


def test_multiple_writes_correctly_merges(snapshot):
    project = Project(files=GOOD_NESTED_DIRS)

    assert project.files == snapshot(name="original_files")

    project.write({
        'another.py': 'Yet another!!!'
    })

    assert project.files == snapshot(name="merged_files")


def test_proper_write_with_dispose(snapshot):
    base_dir = None

    project = Project(files=GOOD_NESTED_DIRS)

    base_dir = project.base_dir

    assert path.exists(base_dir) and path.isdir(base_dir)

    assert project.read() == snapshot

    project.dispose()

    assert not path.exists(base_dir)


def test_read_recreates_project_from_disc(snapshot):
    project = Project(files=GOOD_NESTED_DIRS)

    dir_json = project.read()

    assert dir_json == snapshot


def test_read_recreates_project_from_disc_with_similar_filenames(snapshot):
    files = {
        "valid_file.txt": "some text",
        "sub": {
            "valid_file.txt": "some text",
            "sub": {
                "valid_file.txt": "some text",
            },
        },
    }

    project = Project(files=files)

    dir_json = project.read()

    assert dir_json == snapshot


def test_read_ignore_files(snapshot):
    files = {
        ".git": {"a_nested_dir": {"last_nested_dir": {"a_file": "some text"}}},
        ".github": {"ignore_me": {}, "do_not_ignore_me": {"a_file": "some text"}},
        "ignore_me": "some text",
        "do_not_ignore_me": "some text",
    }

    project = Project(files=files, ignore_patterns=["**/ignore_me"])

    dir_json = project.read()

    assert dir_json == snapshot
