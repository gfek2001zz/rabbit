#!/usr/bin/python

from core.decorator.route import route
from core.http.response import JSONResponse

@route(path="/admin", isClass=True)
class UserController:

    @route(path="/index/(\d+)")
    def indexAction(self, request, id):
        content = 'Hello World, id is %s' % id;

        return JSONResponse(content);