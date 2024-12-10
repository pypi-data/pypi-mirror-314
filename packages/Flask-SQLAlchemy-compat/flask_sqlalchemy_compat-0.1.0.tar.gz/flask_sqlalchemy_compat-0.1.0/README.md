# Flask SQLAlchemy Compat

<p><img alt="Banner" src="https://repository-images.githubusercontent.com/900959960/5fa49b35-0f23-4e6d-9c00-b57ff6e513fd"></p>

<p align="center">
  <a href="https://github.com/cainmagi/flask-sqlalchemy-compat/releases/latest"><img alt="GitHub release (latest SemVer)" src="https://img.shields.io/github/v/release/cainmagi/flask-sqlalchemy-compat?logo=github&sort=semver&style=flat-square"></a>
  <a href="https://github.com/cainmagi/flask-sqlalchemy-compat/releases"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/cainmagi/flask-sqlalchemy-compat/total?logo=github&style=flat-square"></a>
  <a href="https://github.com/cainmagi/flask-sqlalchemy-compat/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/cainmagi/flask-sqlalchemy-compat?style=flat-square&logo=opensourceinitiative&logoColor=white"></a>
  <a href="https://pypi.org/project/flask-sqlalchemy-compat"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/flask-sqlalchemy-compat?style=flat-square&logo=pypi&logoColor=white&label=pypi"/></a>
</p>
<p align="center">
  <a href="https://github.com/cainmagi/flask-sqlalchemy-compat/actions/workflows/python-package.yml"><img alt="GitHub Actions (Build)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/flask-sqlalchemy-compat/python-package.yml?style=flat-square&logo=githubactions&logoColor=white&label=build"></a>
  <a href="https://github.com/cainmagi/flask-sqlalchemy-compat/actions/workflows/python-publish.yml"><img alt="GitHub Actions (Release)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/flask-sqlalchemy-compat/python-publish.yml?style=flat-square&logo=githubactions&logoColor=white&label=release"></a>
</p>

Support the compatibility between `flask_sqlalchemy` and `flask_sqlalchemy_lite`. It allows users to make minimal changes when they need to migrate from either one of these two packages to each other.

The main motivation of this package is because `flask_sqlalchemy_lite` does not support `python<=3.8`. This package is designed for providing the similar usages when users have to make the `flask_sqlalchemy_lite` working with `python<=3.8` by using `flask_sqlalchemy`. In this case, users can get rid of the difficulty of maintaining two sets of codes.

> [!WARNING]
> This package is designed for `sqlalchemy>=2`. If you are using an older version.

> [!WARNING]
> To make this package work with `python=3.7`, users should install an unofficial `flask-sqlalchemy` version.

## 1. Install

Intall the **latest released version** of this package by using the PyPI source:

``` sh
python -m pip install flask-sqlalchemy-compat
```

Or use the following commands to install **the developing version** from the GitHub Source when you have already installed [Git :hammer:][tool-git]:

```sh
python -m pip install "flask-sqlalchemy-compat[dev] @ git+https://github.com/cainmagi/flask-sqlalchemy-compat.git"
```

> [!WARNING]
> To make this package work with `python=3.7`, users should install an unofficial `flask-sqlalchemy` version. See
>
> https://github.com/pallets-eco/flask-sqlalchemy/issues/1140#issuecomment-1577921154
>
> This unofficial version can be installed by:
> ```sh
> python -m pip install flask-sqlalchemy-compat[backends]
> ```
> Note that specifying the option `backends` require `git` when you are using `python=3.7`. Certainly, you do not need `git` if you are using `python>=3.8`.

## 2. Usage

When you are using `flask-sqlalchemy-lite`, using the following codes will let your codes fall back to the compatible mode if `flask-sqlalchemy-lite` is not installed but `flask-sqlalchemy` is installed.

```python
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import flask_sqlalchemy_compat as fsc


class _Base(sa_orm.DeclarativeBase): ...


db, Base = fsc.get_flask_sqlalchemy_lite(_Base)


class NewModel(Base):
    __tablename__ = "new_model"

    id: sa_orm.Mapped[int] = sa_orm.mapped_column(primary_key=True)
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()


if __name__ == "__main__":
    import os
    import flask

    app = flask.Flask(__name__, instance_path=os.path.abspath("./instance"))

    with app.app_context():
        app.config.update({"SQLALCHEMY_ENGINES": {"default": "sqlite:///main.db"}})
        db.init_app(app)

        Base.metadata.create_all(db.engine)

        db.session.add(NewModel(name="new"))
        db.session.commit()

        model = db.session.scalar(sa.select(NewModel))
        print(model.id, model.name) if model is not None else print("NOT FOUND.")
```

The above codes will works no matter `flask_sqlalchemy_lite` or `flask_sqlalchemy` is installed.

Similarly, the following example is designed for the codes written with `flask_sqlalchemy`. The codes fall back to the compatible mode if `flask-sqlalchemy` is not installed but `flask-sqlalchemy-lite` is installed.

```python
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import flask_sqlalchemy_compat as fsc


class _Base(sa_orm.DeclarativeBase): ...


db = fsc.get_flask_sqlalchemy(_Base)


class NewModel(db.Model):
    id: sa_orm.Mapped[int] = sa_orm.mapped_column(primary_key=True)
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()


if __name__ == "__main__":
    import os
    import flask

    app = flask.Flask(__name__, instance_path=os.path.abspath("./instance"))

    with app.app_context():
        app.config.update({"SQLALCHEMY_DATABASE_URI": "sqlite:///main.db"})
        db.init_app(app)
        db.create_all()

        # Indeed, flask_sqlalchemy has a type hint issue until `3.1.x`.
        # But it does not cause issues in run time. See
        # https://github.com/pallets-eco/flask-sqlalchemy/issues/1312
        db.session.add(NewModel(name="new"))
        db.session.commit()

        model = db.session.scalar(sa.select(NewModel))
        print(model.id, model.name) if model is not None else print("NOT FOUND.")
```

The magic happens if you run the first example with only `flask-sqlalchemy` installed and the second example with only `flask-sqlalchemy-lite` installed.

## 3. Documentation

> [!CAUTION]
> The documentation is not accessible now because it is still to be done.

Check the documentation to find more details about the examples and APIs.

https://cainmagi.github.io/flask-sqlalchemy-compat/

## 4. Contributing

See [CONTRIBUTING.md :book:][link-contributing]

## 5. Changelog

See [Changelog.md :book:][link-changelog]

[tool-git]:https://git-scm.com/downloads

[link-contributing]:https://github.com/cainmagi/flask-sqlalchemy-compat/blob/main/CONTRIBUTING.md
[link-changelog]:https://github.com/cainmagi/flask-sqlalchemy-compat/blob/main/Changelog.md
