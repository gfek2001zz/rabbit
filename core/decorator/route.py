#!/usr/bin/python

class Route(object):
    '''
    用于配置路由，在WSGIHandler中根据配置的
    路由来调用不同的控制器
    '''
    def __call__(self, path = '/', isClass = False):
        if isClass:
            def _wrapper(cls):
                setattr(cls, 'c_path', path)

                return cls
            return _wrapper
        else:
            def _wrapper(func):
                def __wrapper(self, *args):
                    path_regex = getattr(self, 'path_regex')
                    if not path_regex:
                        path_regex = dict()

                    c_path = getattr(self, 'c_path').rstrip('/')
                    path_regex[r'^%s%s$' % (c_path, path)] = func
                    setattr(self, 'path_regex', path_regex)
                    
                    func(*args)
                return __wrapper
            return _wrapper
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value


route = Route()