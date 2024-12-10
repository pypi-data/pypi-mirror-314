# candbg



Debugging tools for can bus



## Development


*  develop and test in devcontainer (VSCode)
*  CI
    - trigger ci builds by bumping version with a tag. (see `.gitlab-ci.yml`)
    - run locally on host with `invoke ci`

## Tooling

* Automation: `invoke` - run `invoke -l` to list available commands. (uses `tasks.py`)
* Verisoning : `setuptools_scm`
* Linting and formatting : `ruff`
* Typechecking: `mypy`

## What goes where
* `src/candbg` app code. `pip install .` .
* `tasks.py` automation tasks.



