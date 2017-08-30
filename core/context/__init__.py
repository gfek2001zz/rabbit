#!/usr/bin/python
#coding:utf-8

import os
import logging
import importlib
import re

from core.context import global_settings

ENVIRONMENT_VARIABLE = 'RABBIT_SETTINGS_MODULE'
logger = logging.getLogger('conf.settings')
empty = object()

class RequestContext(object):
    '''
    全局配置参数管理类
    '''
    _wrapper = False
    
    def _setup(self, name=None):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            desc = ("环境变量 %s" % name) if name else "settings"
            raise SettingsExcption(
                "没有设置%s，你可以通过os.environ.set(%s, value)来设置它" 
                % (desc, name)
            )

        self._wrapper = self._loadSettings(settings_module)
        
    def __getattr__(self, name):
        '''
        当访问配置项时，自动获取global_settings
        以及RABBIT_SETTINGS_MODULE所指定settings中的配置项
        '''
        if self._wrapper is False:
            self._setup(name)

        else:
            setattr(self, name, None)

        return self.__dict__[name]

    def _loadSettings(self, settings_module):
        '''
        根据配置将全局配置项读取到类中
        作为当前类的一个属性
        '''
        for setting in dir(global_settings):
            logger.info(setting)
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        tuple_settings = (
            "CONTROLLER_MODULE",
        )

        mod = importlib.import_module(settings_module)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ContextExcepion("配置项%s类型必须是list或者tuple" % setting)
                    
                setattr(self, setting, setting_value)
        
        return True
        



class ContextExcepion(Exception):
    pass

applicationContext = RequestContext()


def load_controller_route(controller_mods):
    '''
    读取各个控制器的路由映射
    '''
    if not controller_mods:
        raise ControllerModuleException("请先在Settings.py配置CONTROLLER_MODULE控制器所在模块")

    for controller_mod in controller_mods:
        mod = importlib.import_module(controller_mod)

        for controller in dir(mod):
            if re.match(r'\w+Controller', controller):
                controller_cls = getattr(mod, controller)()

                for action in dir(controller_cls):
                    if re.match(r'\w+Action', action):
                        args = (applicationContext.ROUTE_SCANNING_MARK,)
                        getattr(controller_cls, action)(controller_cls, *args)

    return True