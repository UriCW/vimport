#!/bin/bash
# A helper to start the celery worker and main application locally.
# Still require dependent services, which you can start with
# $docker compose up redis database mock-file-server 
# You also need to define the database login details, either as environment variables or in a .env file
# POSTGRES_DB="rides"
# POSTGRES_USER="user"
# POSTGRES_PASSWORD="password"
# To match the ones defined in `env.docker`
celery -A app worker --loglevel INFO &
CELERY_PID=$!
python -m flask --app app run &
FLASK_PID=$!

cleanup() {
    kill $CELERY_PID
    kill $FLASK_PID
}

trap cleanup EXIT

wait $CELERY_PID
wait $FLASK_PID
