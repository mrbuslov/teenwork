#!/bin/sh

# ./healthcheck.sh

# gunicorn --log-level info --log-file=- --workers 4 --timeout 300 --name teenwork_gunicorn -b 0.0.0.0:8000 --reload core.wsgi:application

python manage.py runserver 0.0.0.0:8000

python /var/teenwork/manage.py migrate
