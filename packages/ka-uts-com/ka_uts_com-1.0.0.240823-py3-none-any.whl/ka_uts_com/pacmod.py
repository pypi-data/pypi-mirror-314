# coding=utf-8

from os import path as os_path
import pkg_resources

from typing import Any, Dict, List

T_Arr = List[Any]
T_Dic = Dict[Any, Any]

TN_Dic = None | T_Dic


class Pacmod:
    """ Package Module Management
    """
    def sh_d_pacmod(root_cls, tenant: Any) -> T_Dic:
        """ Show Pacmod Dictionary
        """
        a_pacmod: T_Arr = root_cls.__module__.split(".")
        package = a_pacmod[0]
        module = a_pacmod[1]
        d_pacmod: T_Dic = {}
        d_pacmod['tenant'] = tenant
        d_pacmod['package'] = package
        d_pacmod['module'] = module
        return d_pacmod

    # class Cfg:
    #    """ Configuration Sub Class of Package Module Class
    #    """
    @staticmethod
    def sh_path_cfg_yaml(pacmod: T_Dic) -> str:
        """ show directory
        """
        package = pacmod['package']
        module = pacmod['module']

        dir: str = f"{package}.data"

        # print(f"dir = {dir}")
        # print(f"package = {package}")
        # print(f"module = {module}")

        path = pkg_resources.resource_filename(dir, f"{module}.yml")
        return path

    @staticmethod
    def sh_path_keys_yaml(
            pacmod: Any, filename: str = 'keys.yml') -> str:
        """ show directory
        """
        package = pacmod['package']
        dir = f"{package}.data"
        path = pkg_resources.resource_filename(dir, filename)
        return path

    @staticmethod
    def sh_pacmod_type(pacmod: Dict, type_: str) -> str:
        """ show Data File Path
        """
        package = pacmod['package']
        module = pacmod['module']
        return f"/data/{package}/{module}/{type_}"

    @classmethod
    def sh_file_path(
            cls, pacmod: T_Dic, type_: str, suffix: str,
            pid: Any, ts: Any, **kwargs) -> str:
        """ show type specific path
        """
        filename = kwargs.get('filename')
        if filename is not None:
            filename_ = filename
        else:
            filename_ = type_

        sw_run_pid_ts = kwargs.get('sw_run_pid_ts', True)
        if sw_run_pid_ts is None:
            sw_run_pid_ts = True

        # _dir: str = cls.Data.Dir.sh(pacmod, type)
        _dir: str = cls.sh_pacmod_type(pacmod, type_)
        if sw_run_pid_ts:
            # pid = str(Com.pid)
            # ts = str(Com.ts_start)
            file_path = os_path.join(
                _dir, f"{filename_}_{pid}_{ts}.{suffix}")
        else:
            file_path = os_path.join(_dir, f"{filename_}.{suffix}")
        return file_path

    @classmethod
    def sh_pattern(
            cls, pacmod: T_Dic, type_: str, suffix: str, **kwargs) -> str:
        """ show type specific path
        """
        filename = kwargs.get('filename')
        _dir: str = cls.sh_pacmod_type(pacmod, type_)
        path = os_path.join(_dir, f"{filename}*.{suffix}")
        return path

    @staticmethod
    def sh_path_cfg_log(pacmod: TN_Dic = None, filename: str = 'log.yml'):
        """ show directory
        """
        if pacmod is None:
            pacmod = {'package': 'ka_uts_com', 'module': 'com'}
        return pkg_resources.resource_filename(
            f"{pacmod['package']}.data", filename
        )
