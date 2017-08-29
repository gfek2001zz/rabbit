#!/usr/bin/python

from core.decorator.route import route
from core.decorator.produces import produces

@route(path="/admin", isClass=True)
@produces(value = "application/json")
class UserController:

    @route(path="/index/(\d+)")
    def indexAction(self, id):
        return 'Hello World, id is %s' % id