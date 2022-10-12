# python-fixturify-project

[![Build status](https://github.com/scalvert/python-fixturify-project/workflows/build/badge.svg?branch=main&event=push)](https://github.com/scalvert/python-fixturify-project/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/python-fixturify-project.svg)](https://pypi.org/project/python-fixturify-project/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/scalvert/python-fixturify-project/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/scalvert/python-fixturify-project/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/scalvert/python-fixturify-project/releases)
[![License](https://img.shields.io/github/license/scalvert/python-fixturify-project)](https://github.com/scalvert/python-fixturify-project/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

> Dynamic fixture creation for your tests

_A Python port of [node-fixturify-project](https://github.com/stefanpenner/node-fixturify-project)_

## Installation

```bash
pip install -U python-fixturify-project
```

or install with `Poetry`

```bash
poetry add python-fixturify-project --dev
```

## Usage

`python-fixturify-project` is a Python package that provides a way to create dynamic fixtures for your tests. Fixtures are real directories and files, written to a temporary directory.

```python
from python_fixturify_project import Project

dir_json = {
    "valid_file.txt": "some text",
    "nested_dir": {
        "valid_empty_file.txt": "",
        "another_nested_empty_dir": {},
        "another_nested_dir": {
            "last_nested_empty_dir": {},
            "final_text_file.txt": "some text",
        },
    },
}

# create a new project with the given directory structure
project = Project(files=dir_json)
# add new files to the project, merging with the existing directory structure
p.write({
    "new_file.txt": "some text"
})

# read the actual contents on disc
actual_dir_json = p.read()
```

### Ignore Files

By default, the `read()` function will ignore all hidden files and directories in your Project file structure. This can be overridden by using the `ignore_patterns` function parameter, which
takes a list of glob pattern strings. This may be slightly confusing, as glob patterns are normally used in an ***inclusive*** manner when performing file-system searches, however any patterns
provided to the `ignore_patterns` parameter will be used in an ***exclusive*** manner. For example:

```python
files = {
    ".git": {
        "a_nested_dir": {}
    },
    ".github": {
        "ignore_me": {},
        "do_not_ignore_me": {
            "a_file": "some text"
        }
    },
    "ignore_me": "some text",
    "do_not_ignore_me": "some text",
}

project = Project(files=files)

dir_json = project.read(ignore_patterns=["**/.git", "**/.git/**", "**/ignore_me"])  # Default is ["**/.git", "**/.git/**"]

assert dir_json == {
    '.github': {
        'do_not_ignore_me': {
            'a_file': 'some text',
        },
    },
    'do_not_ignore_me': 'some text',
}
```

### Usage when writing tests

`python-fixutrify-project` becomes even more useful when combining it with something like [`syrupy`](https://github.com/tophat/syrupy).

```python
from python_fixturify_project import Project


def test_mutating_project(snapshot):
    project = Project(files=INITIAL_DIR_JSON)

    mutate_files_for_some_reason(p.base_dir)

    # ensure mutations were as expected
    assert project.read() == snapshot
```

Or you can use the `project.get` method to get the path to a file in the project.

```python
from python_fixturify_project import Project

def test_mutating_project(snapshot):
    project = Project(files=INITIAL_DIR_JSON)

    mutate_files_for_some_reason(p.base_dir)

    # ensure mutations were as  for single file
    assert project.get('path/to/a/file.py') == snapshot(name='path/to/a/file.py')
```

## 🛡 License

[![License](https://img.shields.io/github/license/scalvert/python-fixturify-project)](https://github.com/scalvert/python-fixturify-project/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/scalvert/python-fixturify-project/blob/master/LICENSE) for more details.
