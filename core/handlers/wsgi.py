#!/usr/bin/python


import importlib
import re
from core.context import applicationContext
from core.http.request import HttpRequest
from core.http.response import Response404

class WSGIHandler(object):
    '''
    WSGI协议处理器
    在这里根据配置的路由
    来映射到不同的控制器方法
    '''
    def __call__(self, environ, start_repsonse):
        path = environ['PATH_INFO']
        
        path_regex = applicationContext.PATH_REGEX
        for regex, cls_info in path_regex.items():
            match = re.match(regex, path)
            if match:
                urlArgs = match.groups()
                request = HttpRequest(environ)
                args = (request,) + urlArgs

                controller = cls_info[0]
                action = cls_info[1]
                response = action(controller, *args)
                response_headers = list(response.items())

                status = '%d %s' % (response.status_code, response.status_name)
                start_repsonse(status, response_headers)

                return [response.content.encode('utf-8')]
            else:
                response = Response404()
                status = '%d %s' % (response.status_code, response.status_name)
                response_headers = list(response.items())
                start_repsonse(status, response_headers)
                return [response.content.encode('utf-8')]

class ControllerModuleException(Exception):
    pass