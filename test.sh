#! /bin/bash

activate_venv() {
    if [ -f "env/bin/activate" ]; then
        . env/bin/activate
        echo "activate venv"
    else
        echo "no venv found"
        exit 1
    fi
}

if [ "$VIRTUAL_ENV" == "" ]; then
    activate_venv
fi

if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "export environment variables"
    echo "DB_ENGINE" $DB_ENGINE
    echo "DB_HOST" $DB_HOST
    echo "DB_PORT" $DB_PORT
    echo "DB_NAME" $DB_NAME
    echo "DB_USER" $DB_USER
    echo "DB_PASS" $DB_PASS
else
    echo "no .env file found"
    exit 1
fi

python gastronome/manage.py test gastronome/
