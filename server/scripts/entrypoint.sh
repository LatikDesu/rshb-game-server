#!/bin/bash

APP_HOST=${HOST:-0.0.0.0}
APP_PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/app/server/logging.ini}

export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
export APP_MODULE=${APP_MODULE:-"server.wsgi:application"}

sleep 10

/app/server/scripts/migrations.sh
/app/server/scripts/createsuperuser.sh
/app/server/scripts/loaddata.sh

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm --bind "${APP_HOST}:${APP_PORT}" --log-config $LOG_CONFIG "$APP_MODULE"
