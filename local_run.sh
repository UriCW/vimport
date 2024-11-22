#!/bin/bash
# A helper to start the celery worker and main application locally.
# Still require dependent services, which you can start with
# $docker compose up redis database mock-file-server 
# You also need to define the database login details, either as environment variables or in a .env file
# POSTGRES_DB="taxis"
# POSTGRES_USER="user"
# POSTGRES_PASSWORD="password"
# To match the ones defined in `env.docker`
celery -A make_celery worker --loglevel INFO &
python app.py
