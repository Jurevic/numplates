#!/bin/sh
set -e

if [ "$COLLECT_STATIC" == "yes" ] ; then
    /venv/bin/python3 /usr/src/app/manage.py collectstatic --noinput
fi

if [ "$START_CELERY_WORKER" == "yes" ] ; then
	/venv/bin/celery -A numplates worker -f celery.log --detach
fi

if [ "$MIGRATE" == "yes" ] ; then
	/venv/bin/python3 /usr/src/app/manage.py migrate
fi

if [ "$1" == "serve" ]; then
    /venv/bin/gunicorn \
        --access-logfile access.log \
        --error-logfile error.log \
        --workers 4 \
        --bind 0.0.0.0:8000 \
        numplates.wsgi
fi
