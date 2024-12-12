# Opinions

This is a Python library, designed to configure other Python projects with a set of tools to make development easier. Unlike tools like cookiecutter that are designed to _start_ a project the right way, Opinions is designed to keep projects up to date with current tools and configurations as they change over time.

Originally, this tool came out of a frustration at how difficult it was to get Black, isort, pylint and pytest to work nicely together such that I could just run a single command and get told about all the ways I'd screwed up - I now prefer Ruff over the Black/isort/pylint trifecta - but there is still a bit of config that I hate copy-pasting between repos every time I start a new project. I wrote a hacky script that made this easier, which I then rewrote properly as Opinions.

## Getting Started

* Install opinions as a development dependancy - eg, for Poetry:
```
poetry add --dev opinions
```
or with pip:
```
pip install opinions
```
* Apply the config
```
opinions apply
```
* Check if the configured tools have found places where things could be improved:
```
pytest
```

## Goals

* Define a config for code formatting, linting and import sorting so everyone works to the same standard.
* Make it easier to write correct code by promoting the use of type hinting.
* Define a configuration for my editor to format code and sort imports automatically to minimize the amount of effort I need to spend meeting the code standard.
* Highlight formatting, linting and type checking issues by integrating these tools into the testing workflow and editor.
* Provide a "baseline" - the tool should not prevent projects from extending on top of the basic configuration.
* Accept that best practice changes over time, and provide a mechanism to bring old projects up to date.

## The Configuration

* [ruff](https://docs.astral.sh/ruff/), for linting, formatting and import sorting. Default config, except:
  * [`line-length`](https://docs.astral.sh/ruff/settings/#line-length) set to 120 - 80 characters is too cramped
  * Linter rules:
    * `E4`, `E7` and `E9` ([pycodestyle](https://docs.astral.sh/ruff/rules/#error-e))
    * `F` ([pyflakes](https://docs.astral.sh/ruff/rules/#pyflakes-f))
    * `UP` ([pyupgrade](https://docs.astral.sh/ruff/rules/#pyupgrade-up))
    * `S` ([bandit](https://docs.astral.sh/ruff/rules/#flake8-bandit-s))
    * `A` ([flake8-builtins](https://docs.astral.sh/ruff/rules/#flake8-builtins-a))
    * `I` ([isort](https://docs.astral.sh/ruff/rules/#isort-i))
* pytest, configured to run:
  * ruff linter and format checks (using [pytest-ruff](https://pypi.org/project/pytest-ruff/))
  * mypy checks (using [pytest-mypy](https://pypi.org/project/pytest-mypy/))
  * `opinions check` to check if the opinions config is correctly applied
* VSCode configuration to:
  * Recommend the [ruff integration extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) be installed
  * Recommend the [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker) integration extension be installed
  * Use ruff to format and organize imports on save
    * The ruff extension can also automatically fix some linter issues on save - this is explicitly _not_ enabled as part of the configuration, but can be enabled if you want
* If the project is using Poetry
  * Explicitly configure the PyPI repository if no other default source is configured
  * Configure [poetry-dynamic-versioning](https://pypi.org/project/poetry-dynamic-versioning/) to set the project version
* Install [poethepoet](https://pypi.org/project/poethepoet/) and configure it with a `build` task to build source and binary packages

## Versioning and Compatibility

This project uses the following version scheme, based loosely off Semantic Versioning

* The "patch" number will be incremented if the release only includes a minor or patch level upgrade to a dependency (eg, "upgrade mypy from x.y.z to x.y+1.0" or "upgrade pytest from x.y.z to x.y.z+1"), or internal changes that don't impact an interface point (ie, the command line arguments)
* The "minor" number will be incremented (and the "patch" number reset to 0) if the release includes a major-level upgrade to a dependency (eg, "upgrade mypy from x.y.z to x+1.0.0"), if the release changes an interface point in a backwards-compatible way, or if the release adds a new feature
* The "major" number will be incremented (and the "minor" and "patch" numbers reset to 0) if the release changes The Configuration such that users will need to run `opinions apply`, if the release includes a backwards-incompatible change to an interface point, or if the minimum supported version of Python changes

Opinions supports Python 3.10 or newer.