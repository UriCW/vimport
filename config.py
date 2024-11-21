import os
import logging
from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

db_name = environ.get("POSTGRES_DB")
db_user = environ.get("POSTGRES_USER")
db_pass = environ.get("POSTGRES_PASSWORD")


class Config(object):
    # Default to locally running dependent services
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_results=True,
    )
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@localhost/{db_name}"
    BATCH_SIZE: int = 100  # How many lines to read before adding to database


class DevelopmentConfig(Config):
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_results=True,
    )


class DockerConfig(Config):
    # Config to run in a docker compose
    CELERY = dict(
        broker_url="redis://redis:6379",
        result_backend="redis://redis:6379",
        task_ignore_results=True,
    )
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@database/{db_name}"


def get_config() -> str:
    # Helper to pick the right config
    env: str = os.environ.get("ENVIRONMENT", "default").strip()
    print(f"ENV: {env}")

    if env == "development":
        logging.info("Using development config")
        return "config.DevelopmentConfig"
    elif env == "docker":
        print(f"ENV - setting conf: {env}")
        logging.info("Using docker config")
        return "config.DockerConfig"
    elif env == "staging":
        logging.info("Using default config")
        return "config.Config"
    elif env == "production":
        logging.info("Using default config")
        return "config.Config"
    else:
        logging.info("Using default config")
        return "config.Config"
