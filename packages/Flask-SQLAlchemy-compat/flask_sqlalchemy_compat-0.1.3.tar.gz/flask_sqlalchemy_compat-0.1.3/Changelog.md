# Flask SQLAlchemy Compat

{:toc}

## CHANGELOG

### 0.1.3 @ 12/11/2024

#### :wrench: Fix

1. Fix: Previously, running `db.init_app(...)` outside the app context will fail if `db` is provided by the proxy class. Now, the `init_app` can be used without limitations.

#### :floppy_disk: Change

1. Adjust the readme file to make the examples consistent with the `db.init_app` behavior in the new version.

### 0.1.2 @ 12/10/2024

#### :wrench: Fix

1. Fix: Adjust the dependency versions to make the requirements satisfy the usage in `Python=3.13`.

### 0.1.1 @ 12/10/2024

#### :wrench: Fix

1. Fix: Stabilize the backend import when using `Python=3.7`, where the compatible backend will provide an version that would not be overridden by other installations.
2. Fix: Correct the package information. The package should be zip-safe and does not include extra data.
3. Fix: Correct some out-of-date information in the readme file.
4. Fix: Make some type hint excluded from the run time to improve the stability.
5. Fix: Adjust the dependency versions to match the requirements specified in `flask-sqlalchemy-lite`.

#### :floppy_disk: Change

1. Add more files to the exclude list of `black`.

### 0.1.0 @ 12/09/2024

#### :mega: New

1. Create this project.
2. Finish the first version of the pacakge `flask-sqlalchemy-compat`.
3. Add configurations `pyproject.toml`.
4. Add the devloper's environment folder `./docker` and the `Dockerfile`.
5. Add the community guideline files: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SECURITY.md`.
6. Add the issue and pull request templates.
7. Configure the github workflows for publishing the package.
8. Add the banner and adjust the format in the readme.

#### :wrench: Fix

1. Fix: Adjust the formats of the `requirements` to make them compatible with `pyproject.toml`.
2. Fix: A Git-sourced dependency is not approved by PyPI. Therefore, replace the Git source by a customized related package: [`Flask-SQLAlchemy-compat-backend-py37`](https://pypi.org/project/Flask-SQLAlchemy-compat-backend-py37).

#### :floppy_disk: Change

1. Adjust the metadata according to the current project status.
