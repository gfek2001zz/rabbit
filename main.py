#!/usr/bin/python
import os
import sys

from core.servers.httpserver import run
from core.handlers.wsgi import WSGIHandler
from core.context import load_controller_route, applicationContext

if __name__ == '__main__':
    os.environ.setdefault('RABBIT_SETTINGS_MODULE', 'blog.settings')
    load_controller_route(applicationContext.CONTROLLER_MODULE)


    run('127.0.0.1', 10503, WSGIHandler())

    
    