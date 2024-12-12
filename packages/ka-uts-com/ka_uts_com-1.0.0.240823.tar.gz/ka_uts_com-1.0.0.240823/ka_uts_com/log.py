from ka_uts_com.com import Com

from typing import Any, Callable


class Log:
    """Logging Class
    """
    class Eq:

        @staticmethod
        def sh(key: Any, value: Any) -> str:
            """ Show Key, Value as Equate
            """
            return f"{key} = {value}"

        @classmethod
        def debug(cls, key: Any, value: Any) -> None:
            Log.debug(cls.sh(key, value), stacklevel=3)

        @classmethod
        def error(cls, key: Any, value: Any) -> None:
            Log.error(cls.sh(key, value), stacklevel=3)

        @classmethod
        def info(cls, key: Any, value: Any) -> None:
            Log.info(cls.sh(key, value), stacklevel=3)

        @classmethod
        def warning(cls, key: Any, value: Any) -> None:
            Log.warning(cls.sh(key, value), stacklevel=3)

    @staticmethod
    def debug(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        fnc_debug: Callable = Com.Log.debug
        fnc_debug(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        fnc_error: Callable = Com.Log.error
        fnc_error(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        fnc_info: Callable = Com.Log.info
        fnc_info(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        fnc_warning: Callable = Com.Log.warning
        fnc_warning(*args, **kwargs)
