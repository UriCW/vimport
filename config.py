"""Flask config."""

from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_results=True,
    )
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
