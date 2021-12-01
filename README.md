# BankTrack

## Pre-commit

We use [pre-commit](https://pre-commit.com/) for linting. The following checks are added: trailing white spaces, end of files, yaml, large files, [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/), [isort](https://pycqa.github.io/isort/), [mypy](http://www.mypy-lang.org/) and [docstyle](http://www.pydocstyle.org/en/stable/).

Install pre-commit locally with `pip install pre-commit` or on MacOS `brew install pre-commit`.

Run `pre-commit install` to set up the git hook scripts.

Run pre-commit against git diff:

```
pre-commit
```

Run pre-commit against all files:

```
pre-commit run --all-files
```

## Poetry

[Poetry](https://python-poetry.org/) is a package manager that makes dependecy management easier.

Install poetry in your global environment and point it to your local Python version of choice:

```shell
pip install poetry==1.2.0a2 poetry-dynamic-versioning
poetry env use [location/of/python/version/bin/python]
```

Before you start, add export POETRY_VIRTUALENVS_IN_PROJECT=1 to your .bash_profile, .bashrc, etc to make sure poetry creates the venv in this project folder and your IDE can auto-discover it. It will be kept out of source control.

You can also use e.g. pyenv or virtualenv to manage Python versions (might have to upgrade the latter) and point poetry to that. Refer to the docs on how to set the right Python env: https://python-poetry.org/docs/managing-environments/.
