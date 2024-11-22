#!/bin/bash
# A helper to start the celery worker and main application locally.
# Still require dependent services, which you can start with
# $docker compose up redis database mock-file-server
celery -A make_celery worker --loglevel INFO &
python app.py
