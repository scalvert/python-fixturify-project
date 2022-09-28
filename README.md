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
with Project(files=dir_json) as p:
  # add new files to the project, merging with the existing directory structure
  p.write({
      "new_file.txt": "some text"
  })

  # read the actual contents on disc
  actual_dir_json = p.read()
```

### Ignore Files

By default, the `read()` function will ignore all `.git` directories in your Project file structure. This can be overridden by using the `ignore_patterns` function parameter, which
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

with Project(files=files) as p:

    dir_json = p.read(ignore_patterns=["**/.git", "**/.git/**", "**/ignore_me"])  # Default is ["**/.git", "**/.git/**"]

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
    with Project(files=INITIAL_DIR_JSON) as p:
      mutate_files_for_some_reason(p.base_dir)

      # ensure mutations were as expected
      assert project.read() == snapshot
```

## Development

### Makefile usage

[`Makefile`](https://github.com/scalvert/python-fixturify-project/blob/main/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/scalvert/python-fixturify-project/tree/main/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 🛡 License

[![License](https://img.shields.io/github/license/scalvert/python-fixturify-project)](https://github.com/scalvert/python-fixturify-project/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/scalvert/python-fixturify-project/blob/master/LICENSE) for more details.
