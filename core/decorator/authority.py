#!/usr/bin/python
# -*- coding:utf-8 -*-

class Resource:
    '''用于Controller的权限控制装饰器'''
    def __call__(code, desc, is_scan = False):
        def _warpper(cls):
            print code, desc
            return cls
            
        return _warpper

class Operation:
    '''用于Action的权限控制的装饰器'''
    def __call__(code, desc, is_scan = False):
        def _wrapper(func):
            def __wrapper(self, *args, **kwargs):
                print code, desc
                #if is_scan:
                #else:
                func(self, *args, **kwargs)
            return __wrapper

        return _wrapper

rabbit_resource = Resource()
rabbit_operation = Operation()