# coding=utf-8

from typing import Any, Callable, Dict

T_Dic = Dict[Any, Any]
T_DicStr2Callable = Dict[str, Callable]

TN_Str = None | str
TN_Callable = None | Callable


class Fnc:
    """ Manage Functions
    """
    @staticmethod
    def sh(d_key2fnc: T_DicStr2Callable, key: TN_Str) -> Callable:
        if not key:
            msg = f"key {key} is None or empty string"
            raise Exception(msg)
        _fnc: TN_Callable = d_key2fnc.get(key)
        if not _fnc:
            msg = f"key {key} is not defined in function table {d_key2fnc}"
            raise Exception(msg)
        else:
            return _fnc

    @staticmethod
    def ex(d_key2fnc: T_DicStr2Callable, key: TN_Str, kwargs: T_Dic) -> None:
        if not key:
            msg = f"key {key} is None or empty string"
            raise Exception(msg)
        _fnc: TN_Callable = d_key2fnc.get(key)
        if not _fnc:
            msg = f"key {key} is not defined in function table {d_key2fnc}"
            raise Exception(msg)
        else:
            _fnc(kwargs)
