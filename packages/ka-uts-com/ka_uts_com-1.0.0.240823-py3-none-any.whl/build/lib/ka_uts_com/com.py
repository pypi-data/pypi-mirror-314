# coding=utf-8

import calendar
import logging
import logging.config
from logging import Logger

import os
import time
from datetime import datetime

from ka_uts_com.ioc import Yaml
from ka_uts_com.ioc import Jinja2
from ka_uts_com.pacmod import Pacmod

from typing import Any, Callable, List, Dict

T_Any = Any
T_Arr = List[Any]
T_Bool = bool
T_Dic = Dict[Any, Any]

TN_Arr = None | T_Arr
TN_Bool = None | bool
TN_Dic = None | T_Dic
TN_DT = None | datetime


class LogStandard:
    """Standard Logging
    """
    sw_init: bool = False
    cfg: T_Dic = {}
    log: Logger = logging.getLogger('dummy_logger')
    logfile: str = 'log.standard.yml'

    @staticmethod
    def read(pacmod: T_Dic, filename: str) -> Any:
        """Read log file path with jinja2
        """
        # path: str = Pacmod.Path.Log.sh_cfg(filename=filename)
        path: str = Pacmod.sh_path_cfg_log(filename=filename)
        tenant: str = pacmod['tenant']
        package: str = pacmod['package']
        module: str = pacmod['module']
        pid = Com.pid
        ts: TN_DT = Com.ts_start
        cfg = Jinja2.read(
            path, tenant=tenant,
            package=package, module=module,
            pid=pid, ts=ts)
        return cfg

    @classmethod
    def set_level(cls, sw_debug: bool) -> None:
        """Set static variable log level in log configuration handlers
        """
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        cls.cfg['handlers']['main_debug_console']['level'] = level
        cls.cfg['handlers']['main_debug_file']['level'] = level

    @classmethod
    def init(
            cls, **kwargs) -> None:
        cls.sw_init = True
        cls.cfg = cls.read(Com.pacmod_curr, cls.logfile)
        sw_debug: Any = kwargs.get('sw_debug')
        cls.set_level(sw_debug)
        logging.config.dictConfig(cls.cfg)
        cls.log = logging.getLogger('main')

    @classmethod
    def sh(cls, **kwargs) -> Any:
        if cls.sw_init:
            return cls.log
        cls.init(**kwargs)
        return cls.log


class LogPersonal:
    """Personal Logging
    """
    sw_init: bool = False
    cfg: T_Dic = {}
    logfile = 'log.person.yml'
    log: Logger = logging.getLogger('dummy_logger')

    @classmethod
    def read(cls, pacmod: T_Dic, person: Any, filename: str) -> Any:
        path: str = Pacmod.sh_path_cfg_log(filename=filename)
        package: str = pacmod['package']
        module: str = pacmod['module']
        return Jinja2.read(
            path, package=package, module=module, person=person,
            pid=Com.pid, ts=Com.ts_start)

    @classmethod
    def set_level(cls, person: str, sw_debug: bool) -> None:
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        cls.cfg['handlers'][f'{person}_debug_console']['level'] = level
        cls.cfg['handlers'][f'{person}_debug_file']['level'] = level

    @classmethod
    def init(cls, pacmod: T_Dic, person: str, sw_debug: bool) -> None:
        cls.cfg = cls.read(pacmod, person, cls.logfile)
        cls.set_level(person, sw_debug)
        logging.config.dictConfig(cls.cfg)
        cls.log = logging.getLogger(person)

    @classmethod
    def sh(cls, **kwargs) -> Any:
        if cls.sw_init:
            return cls.log
        cls.init(**kwargs)
        return cls.log


class Cfg:
    """Configuration Class
    """
    @classmethod
    def init(cls, pacmod: T_Dic) -> TN_Dic:
        """ the package data directory has to contain a __init__.py
            file otherwise the objects notation {package}.data to
            locate the package data directory is invalid
        """
        _dic: TN_Dic = Yaml.read(Pacmod.sh_path_cfg_yaml(pacmod))
        return _dic


class Mgo:
    """Mongo DB Class
    """
    client = None


class App:
    """Aplication Class
    """
    sw_init: T_Bool = False
    httpmod: T_Any = None
    sw_replace_keys: TN_Bool = None
    keys: TN_Arr = None
    reqs: T_Dic = {}
    app: T_Dic = {}

    @classmethod
    def init(cls, **kwargs) -> Any:
        cls.sw_init = True
        cls.httpmod = kwargs.get('httpmod')
        cls.sw_replace_keys = kwargs.get('sw_replace_keys', False)
        try:
            if cls.sw_replace_keys:
                pacmod = kwargs.get('pacmod_curr')
                # cls.keys = Yaml.read(Pacmod.Pmd.sh_path_keys(pacmod))
                cls.keys = Yaml.read(Pacmod.sh_path_keys_yaml(pacmod))
        except Exception as e:
            if Com.Log is not None:
                fnc_error: Callable = Com.Log.error
                fnc_error(e, exc_info=True)
            raise
        return cls

    @classmethod
    def sh(cls, **kwargs) -> Any:
        if cls.sw_init:
            return cls
        cls.init(**kwargs)
        return cls


class Exit:
    """Exit Class
    """
    sw_critical: bool = False
    sw_stop: bool = False
    sw_interactive: bool = False


class Com:
    """Communication Class
    """
    sw_init: bool = False
    cfg: TN_Dic = None
    pid = None
    pacmod_curr: T_Dic = {}

    ts_start: None | datetime = None
    ts_end: None | datetime = None
    ts_etime: None | datetime = None
    d_timer: Dict = {}

    # Log = None
    Log: Logger = logging.getLogger('dummy_logger')
    App = None
    Exit = Exit

    @classmethod
    def init(cls, **kwargs):
        """ set log and application (module) configuration
        """
        if cls.sw_init:
            return
        cls.sw_init = True

        cls.pacmod_curr = kwargs.get('pacmod_curr')
        cls.ts_start = calendar.timegm(time.gmtime())
        cls.pid = os.getpid()

        cls.cfg = Cfg.init(cls.pacmod_curr)
        log_type = kwargs.get('log_type', 'standard')
        if log_type == 'standard':
            cls.Log = LogStandard.sh(**kwargs)
        else:
            cls.Log = LogPersonal.sh(**kwargs)
        cls.App = App.sh(**kwargs)
