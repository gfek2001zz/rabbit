#!/usr/bin/python

import importlib
import re
from core.context import applicationContext


class WSGIHandler(object):

    def __call__(self, environ, start_repsonse):
        path = environ['PATH_INFO']

        path_regex = applicationContext.PATH_REGEX
        for regex, func in path_regex.items():
            match = re.match(regex, path)
            if match:
                args = match.groups()
                response_body = func(self, *args)

                # HTTP response code and message
                status = '200 OK'
                
                # 应答的头部是一个列表，每对键值都必须是一个 tuple。
                response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                                    ('Content-Length', str(len(response_body)))]
                
                # 调用服务器程序提供的 start_response，填入两个参数
                start_repsonse(status, response_headers)
                
                return [response_body.encode('utf-8')]
            
            start_repsonse("404 NOT FOUND",[('Content-type', 'text/plain')])            
            return ["page dose not exists".encode('utf-8')]


class ControllerModuleException(Exception):
    pass
            
            
        
        



        
        
