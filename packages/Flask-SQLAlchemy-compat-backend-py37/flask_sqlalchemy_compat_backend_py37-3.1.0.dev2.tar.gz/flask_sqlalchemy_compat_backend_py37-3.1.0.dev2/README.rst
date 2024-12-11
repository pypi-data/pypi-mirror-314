Flask-SQLAlchemy-compat-backend-py37
====================================

Flask SQLAlchemy backend supporting the Python 3.7 version of Flask
SQLAlchemy compat.

This package is forked from an unofficial version of Flask SQLAlchemy. The
motication of uploading this fork to PyPI includes:

1. Bring the `DeclarativeBase` feature to Python 3.7. The official version is
up to 3.0.5 which is not compatible with the ``sqlalchemy2`` style.

2. Serve as a backend support of the package `flask-sqlalchemy-compat` when using
Python 3.7

If you are using ``Pyhon<3.7``, you should not use `flask-sqlalchemy-compat`, the
only available choice is `flask-sqlalchemy`.

If you are using ``Python>=3.8``, you do not need this package, because
``flask-sqlalchemy`` is already compatible with ``Python>=3.8``.

+---------------------------------+
| Reference                       |
+=================================+
| `Flask SQLAlchemy compat`_      |
+---------------------------------+
| `Forked from Flask SQLAlchemy`_ |
+---------------------------------+
| `See details of this version`_  |
+---------------------------------+

.. _Flask SQLAlchemy compat: https://github.com/cainmagi/flask-sqlalchemy-compat
.. _Forked from Flask SQLAlchemy: https://github.com/pamelafox/flask-sqlalchemy/tree/fdeec1d0d98669cc612e1f69d6875f9c1e4c6c45
.. _See details of this version: https://github.com/pallets-eco/flask-sqlalchemy/issues/1140#issuecomment-1577921154

Flask-SQLAlchemy
----------------

    | The following part is from the original README file.

Flask-SQLAlchemy is an extension for `Flask`_ that adds support for
`SQLAlchemy`_ to your application. It aims to simplify using SQLAlchemy
with Flask by providing useful defaults and extra helpers that make it
easier to accomplish common tasks.

.. _Flask: https://palletsprojects.com/p/flask/
.. _SQLAlchemy: https://www.sqlalchemy.org


Installing
----------

Install and update using `pip`_:

.. code-block:: text

  $ pip install -U Flask-SQLAlchemy

.. _pip: https://pip.pypa.io/en/stable/getting-started/


A Simple Example
----------------

.. code-block:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"

    class Base(DeclarativeBase):
      pass

    db = SQLAlchemy(app, model_class=Base)

    class User(db.Model):
        id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
        username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

    with app.app_context():
        db.create_all()

        db.session.add(User(username="example"))
        db.session.commit()

        users = db.session.execute(db.select(User)).scalars()


Contributing
------------

For guidance on setting up a development environment and how to make a
contribution to Flask-SQLAlchemy, see the `contributing guidelines`_.

.. _contributing guidelines: https://github.com/pallets-eco/flask-sqlalchemy/blob/main/CONTRIBUTING.rst


Donate
------

The Pallets organization develops and supports Flask-SQLAlchemy and
other popular packages. In order to grow the community of contributors
and users, and allow the maintainers to devote more time to the
projects, `please donate today`_.

.. _please donate today: https://palletsprojects.com/donate


Links
-----

-   Documentation: https://flask-sqlalchemy.palletsprojects.com/
-   Changes: https://flask-sqlalchemy.palletsprojects.com/changes/
-   PyPI Releases: https://pypi.org/project/Flask-SQLAlchemy/
-   Source Code: https://github.com/pallets-eco/flask-sqlalchemy/
-   Issue Tracker: https://github.com/pallets-eco/flask-sqlalchemy/issues/
-   Website: https://palletsprojects.com/
-   Twitter: https://twitter.com/PalletsTeam
-   Chat: https://discord.gg/pallets
