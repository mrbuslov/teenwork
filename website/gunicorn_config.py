command = '/home/buslov/code/website/env/bin/gunicorn'
pythonpath = '/home/buslov/code/website/website'
bind = '127.0.0.1:8001'
workers = 3 # 2 * кол-во ядер + 1
user = 'buslov'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=website.settings'
timeout = 900