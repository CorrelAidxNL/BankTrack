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
