# How to contribute

### Tasks usage

[`Taskfile.yml`](https://github.com/scalvert/python-fixturify-project/blob/main/Taskfile.yml) contains a lot of functions for faster development.

| Task Name            | Description                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| `poetry-download`    | Downloads and installs Poetry.                                                                              |
| `poetry-remove`      | Uninstalls Poetry.                                                                                          |
| `install`            | Locks dependencies with Poetry, exports them to `requirements.txt`, and installs them. Runs `mypy` as well. |
| `pre-commit-install` | Installs pre-commit hooks using Poetry.                                                                     |
| `format`             | Runs formatters (`pyupgrade`, `isort`, `black`) on Python files.                                            |
| `test`               | Runs tests with pytest and generates a coverage report and badge.                                           |
| `update-snapshot`    | Updates test snapshots using pytest.                                                                        |
| `check-codestyle`    | Checks code style with `isort`, `black`, and `darglint`.                                                    |
| `mypy`               | Runs type checks using `mypy`.                                                                              |
| `check`              | Runs various checks (`poetry check` and `bandit`) on the project.                                           |
| `lint`               | Aggregates linting tasks: code style check, `mypy`, and general checks.                                     |
| `update-dev-deps`    | Updates development dependencies to their latest versions using Poetry.                                     |
| `clean`              | Removes various cache and temporary files from the project directory.                                       |

## Dependencies

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you dont have `poetry`, you should install with `task poetry-download`.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run `install` command:

```bash
task install
task pre-commit-install
```

To activate your `virtualenv` run `poetry shell`.

## Format

After installation you may execute code formatting.

```bash
task format
```

### Checks

Many checks are configured for this project. Command `task check-codestyle` will check black, isort and darglint.

Comand `task lint` applies all checks.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Run `task codestyle` to format your changes.
1. Run `task lint` to ensure that types, security and docstrings are okay.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
