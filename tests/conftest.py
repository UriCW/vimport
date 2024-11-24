import os
import pytest
from app import create_app, db, celery_app

os.environ["ENVIRONMENT"] = "test"


@pytest.fixture
def app():
    app = create_app("test")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def celery_worker():
    celery_app.conf.update(task_always_eager=True)
    yield celery_app
    celery_app.conf.update(task_always_eager=False)
