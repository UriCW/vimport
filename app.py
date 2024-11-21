import os
import time
from flask import Flask, request
from celery import Celery, Task, shared_task
from celery.result import AsyncResult
import pandas as pd
from models import db, migrate, TripRecord
from sqlalchemy.orm import sessionmaker


@shared_task(ignore_results=False, bind=True)
def import_csv_task(self, url: str, batch_size: int = 100):
    """This task imports the CSV to database"""
    processed = 0
    engine = db.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    datetime_columns = [
        "request_datetime",
        "on_scene_datetime",
        "pickup_datetime",
        "dropoff_datetime",
    ]
    with pd.read_csv(url, chunksize=1, parse_dates=datetime_columns) as reader:
        for chunk in reader:
            records = chunk.to_dict(orient="records")
            # Pandas like to use it's own none types (NaN, NaT) on missing keys which SQLAlchemy doesn't understand
            # Convert to python None
            records = [
                {k: (v if not pd.isna(v) else None) for k, v in rec.items()}
                for rec in records
            ]

            objs = [TripRecord(**rec) for rec in records]
            session.bulk_save_objects(objs)
            session.commit()
            processed += len(records)
            self.update_state(state="PROGRESS", meta={"processed": processed})


def create_celery_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(config="dev") -> Flask:
    app = Flask(__name__)

    # Set correct config for environment
    if config == "dev":
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object("config.Config")
    celery_app = create_celery_app(app)

    # database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Nice import for flask shell access:w
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.route("/health")
    def health():
        return {}

    @app.route("/import", methods=["GET", "POST"])
    def import_csv():
        if request.method == "GET":
            return {
                "message": "Please use a POST request with a URL of a CSV to import"
            }

        if request.method == "POST":
            request_payload = request.json
            print(request_payload)
            if not request_payload or not request_payload.get("target"):
                return {
                    "message": "Request content must contain a 'target' key with a URL for a valid CSV file"
                }, 400
            target_url = request_payload["target"]
            result = import_csv_task.delay(target_url)
            return {"result": result.id}
        return {}

    @app.route("/status/<job_id>")
    def import_status(job_id: str):
        # result = AsyncResult(job_id, app=app)
        result = AsyncResult(job_id)
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
        # revoke(job_id, terminate=True)
        return {}

    return app


if __name__ == "__main__":
    app = create_app()
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
