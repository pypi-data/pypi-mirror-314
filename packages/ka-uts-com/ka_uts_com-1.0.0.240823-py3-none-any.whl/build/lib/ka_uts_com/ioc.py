# coding=utf-8

import jinja2
import os
import yaml

from typing import Any, Dict

T_Dic = Dict[Any, Any]

TN_Any = None | Any


class Yaml:

    """ Manage Object to Yaml file affilitation
    """
    @staticmethod
    def load_with_safeloader(string: str) -> None | Any:
        _obj = yaml.load(string, Loader=yaml.SafeLoader)
        return _obj

    @staticmethod
    def read(path: str) -> TN_Any:
        with open(path) as fd:
            # The Loader parameter handles the conversion from YAML
            # scalar values to Python object format
            _obj = yaml.load(fd, Loader=yaml.SafeLoader)
            return _obj
        return None


class Jinja2:
    """ Manage Object to Json file affilitation
    """
    @staticmethod
    def read_template(
            path: str) -> Any:
        dir, file = os.path.split(path)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(dir))
        return env.get_template(file)

    @classmethod
    def read(
            cls, path: str, **kwargs):
        try:
            # read jinja template from file
            template = cls.read_template(path)

            # render template as yaml string
            template_rendered = template.render(**kwargs)

            # parse yaml string as dictionary
            dic = Yaml.load_with_safeloader(template_rendered)
            return dic
        except Exception:
            raise
