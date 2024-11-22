#!/bin/bash
# A helper for development, start dependent services without the application or the celery worker
# If you haven't already created the datanase, you'll also need to run
# $docker compose up database-migrate 
docker compose up redis database mock-file-server
