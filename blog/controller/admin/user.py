#!/usr/bin/python

from core.decorator.route import route
from core.context.base import BaseController

@route(path="/admin", isClass=True)
class UserController(BaseController):

    @route(path="/index/(\d+)")
    def indexAction(self, id):
        return 'Hello World, id is %s' % id