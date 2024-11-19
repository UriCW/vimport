import os
import csv
from flask import Flask, request
from celery import Celery, Task, shared_task
from celery.result import AsyncResult
import time


def batch_import(url: str):
    pass


@shared_task(ignore_results=False, bind=True)
def import_csv_task(self, url: str) -> int:
    iteration = 0
    for i in range(1, 100):
        time.sleep(1)
        iteration += 1
        with open("/tmp/lala.txt", "w") as fp:
            fp.write(f"Iteration {iteration}")
        print(f"iterations {iteration}")
    return iteration


def create_celery_app(app: Flask) -> Celery:
    # class FlaskTask(Task):
    #     def __call__(self, *args: object, **kwargs: object) -> object:
    #         with app.app_context():
    #             return self.run(*args, **kwargs)

    # celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(config="dev") -> Flask:
    app = Flask(__name__)

    if config == "dev":
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object("config.Config")
    celery_app = create_celery_app(app)

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

        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }

    @app.route("/abort/<job_id>")
    def abort_import(job_id: str):
        return {}

    return app


if __name__ == "__main__":
    app = create_app()
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
