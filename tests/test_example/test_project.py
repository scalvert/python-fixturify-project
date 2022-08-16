"""Tests for Project class."""
from python_fixturify_project.project import Project


def test_project():
    """Example test with parametrization."""
    project = Project()
    assert isinstance(project, Project)
