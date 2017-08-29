#!/usr/bin/python

from core.context import applicationContext

class Route(object):

    _wrapper = None

    '''
    用于配置路由，在WSGIHandler中根据配置的
    路由来调用不同的控制器
    '''
    def __call__(self, path = '/', isClass = False):
        if isClass:
            def _wrapper(cls):
                self._wrapper = path

                return cls
            return _wrapper
        else:
            def _wrapper(func):
                def __wrapper(self, *args):
                    '''
                    在路由装饰器中，将各个控制器路由配置
                    封装城一个dict
                    用于映射各个Action
                    '''
                    path_regex = getattr(applicationContext, 'PATH_REGEX')
                    if path_regex is None:
                        path_regex = {}

                    regex = r'^%s%s$' % (route.getWrapper(), path);
                    if regex not in path_regex:
                        path_regex[regex] = (self, func)
                        setattr(applicationContext, 'PATH_REGEX', path_regex)
                    
                    func(*args)
                return __wrapper
            return _wrapper
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    
    def getWrapper(self):
        return self._wrapper


route = Route()