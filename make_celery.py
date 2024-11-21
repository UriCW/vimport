from app import create_app, db

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
