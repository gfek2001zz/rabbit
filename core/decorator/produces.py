#!/usr/bin/python

class Produces:
    def __call__(self, value = "text/html"):
        def _wrapper(cls):
            setattr(cls, 'content_type', value)

            return cls
        return _wrapper

produces = Produces()

