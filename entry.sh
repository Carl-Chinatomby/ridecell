#!/bin/bash
set -e -o pipefail

# Wait for DB to initialize -- takes a few seconds on the first run.
function wait_for_db {
    while ! nc -z db 5432; do
    sleep 1
    echo "Waiting for PostgreSQL to initialize.."
    done
}

export -f wait_for_db
timeout 25s bash -c wait_for_db


/opt/venv/bin/python scooters/manage.py makemigrations
/opt/venv/bin/python scooters/manage.py migrate
/opt/venv/bin/python scooters/manage.py loaddata scooters.json
/opt/venv/bin/python scooters/manage.py runserver 0.0.0.0:8000
