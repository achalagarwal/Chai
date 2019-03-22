import os
import sys
os.chdir(os.path.dirname(__file__))
command = '/home/ubuntu/virtual_environments/sku/bin/gunicorn'
pythonpath = '/home/ubuntu/frappe/extracter/django_wrapper'
bind = '127.0.0.1:8060'
workers = 2
user = 'nobody'
