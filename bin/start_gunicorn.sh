#!/bin/bash
source /home/buslov/code/website/env/bin/activate
exec gunicorn  -c "/home/buslov/code/website/website/gunicorn_config.py" website.wsgi
