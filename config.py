"""Flask config."""

import os
from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

db_name = environ.get("POSTGRES_DB")
db_user = environ.get("POSTGRES_USER")
db_pass = environ.get("POSTGRES_PASSWORD")


class Config:
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_results=True,
    )

    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@localhost/{db_name}"
    # SQLALCHEMY_DATABASE_URI = environ.get(
    #     "DATABASE_URL", f"sqlite:///{basedir}/db.sqlite3"
    # )
    batch_size: int = 100  # How many lines to read before adding to database


class DevelopmentConfig(Config):
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_results=True,
    )


class ConfigDocker(Config):
    CELERY = dict(
        broker_url="redis://redis:6379",
        result_backend="redis://redis:6379",
        task_ignore_results=True,
    )
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@database/{db_name}"
