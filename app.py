import os
import httpx
import logging
from itertools import islice
from flask import Flask, request
from celery import Celery, Task, shared_task
from celery.result import AsyncResult
from sqlalchemy.orm import sessionmaker

from models import db, migrate, TripRecord
from config import get_config

celery_app = Celery()


def insert_batch(batch):
    engine = db.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    objs = [TripRecord(**rec) for rec in batch]
    session.bulk_save_objects(objs)
    session.commit()


@shared_task(ignore_results=False, bind=True)
def stream_csv(self, url: str, batch_size: int = 100) -> None:
    processed: int = 0
    with httpx.Client() as client:
        with client.stream("GET", url, follow_redirects=True) as stream:
            lines = stream.iter_lines()
            headings = next(lines).split(",")
            while True:
                batch = list(islice(lines, batch_size))
                if not batch:
                    break

                objs = [dict(zip(headings, o.split(","))) for o in batch]
                # Consider doing this as another celery task for performance
                # Insert to database
                insert_batch(objs)

                # Update task status
                processed += len(batch)
                self.update_state(state="PROGRESS", meta={"processed": processed})


def create_celery_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> None:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = FlaskTask
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(config="dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())
    celery_app = create_celery_app(app)

    # database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Nice import for flask shell access
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.route("/health")
    def health():
        app.logger.error(app.config)
        # Should actually check it is *cough cough*
        return {"status": "healthy"}

    @app.route("/import", methods=["GET", "POST"])
    def import_csv():
        if request.method == "GET":
            return {
                "message": "Please use a POST request with a URL of a CSV to import"
            }
        if request.method == "POST":
            request_payload = request.json
            if not request_payload or not request_payload.get("target"):
                return {
                    "message": "Request content must contain a 'target' key with a URL for a valid CSV file"
                }, 400
            target_url = request_payload["target"]
            logging.info(f"Starting import job for {target_url}")
            result = stream_csv.delay(target_url, batch_size=app.config["BATCH_SIZE"])
            return {"task-id": result.id}
        return {}

    @app.route("/status/<job_id>")
    def import_status(job_id: str):
        result: AsyncResult = AsyncResult(job_id)
        if result.state == "PROGRESS":
            processed = result.info.get("processed", 0)
            return {"processed": processed}

        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }

    @app.route("/abort/<job_id>")
    def abort_import(job_id: str):
        celery_app.control.revoke(job_id, terminate=True)
        return {}

    return app


flask_app = create_app()
