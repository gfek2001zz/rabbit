#!/usr/bin/python

class BaseController:

    def __getattr__(self, name):
        '''
        当访问配置项时，自动获取global_settings
        以及RABBIT_SETTINGS_MODULE所指定settings中的配置项
        '''
        setattr(self, name, None)
        return self.__dict__[name]
    
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value