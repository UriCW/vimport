""" Application configurations """

import os
import logging
from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

db_name = environ.get("POSTGRES_DB")
db_user = environ.get("POSTGRES_USER")
db_pass = environ.get("POSTGRES_PASSWORD")


class Config:  # pylint: disable = R0903
    """Base configurations"""

    # Default to locally running dependent services
    CELERY = {
        "broker_url": "redis://localhost",
        "result_backend": "redis://localhost",
        "task_ignore_results": True,
    }
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@localhost/{db_name}"
    BATCH_SIZE: int = 100  # How many lines to read before adding to database


class DevelopmentConfig(Config):  # pylint: disable = R0903
    """Configurations for development"""

    CELERY = {
        "broker_url": "redis://localhost",
        "result_backend": "redis://localhost",
        "task_ignore_results": True,
    }


class DockerConfig(Config):  # pylint: disable = R0903
    """Configurations for Running in docker"""

    # Config to run in a docker compose
    CELERY = {
        "broker_url": "redis://redis:6379",
        "result_backend": "redis://redis:6379",
        "ask_ignore_results": True,
    }
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@database/{db_name}"


class TestConfig(Config):  # pylint: disable = R0903
    """Configurations for Running in tests"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config() -> str:
    """Helper to pick the right config from env ENVIRONMENT"""
    env: str = os.environ.get("ENVIRONMENT", "default").strip()

    if env == "development":
        logging.info("Using development config")
        return "config.DevelopmentConfig"
    if env == "docker":
        logging.info("Using docker config")
        return "config.DockerConfig"
    if env == "test":
        logging.info("Using test config")
        return "config.TestConfig"
    if env == "staging":
        logging.info("Using default config")
        return "config.Config"
    if env == "production":
        logging.info("Using default config")
        return "config.Config"

    logging.info("Using default config")
    return "config.Config"
