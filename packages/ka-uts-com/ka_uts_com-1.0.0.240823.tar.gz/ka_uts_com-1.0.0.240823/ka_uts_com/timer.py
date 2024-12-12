# coding=utf-8

from datetime import datetime

from ka_uts_com.com import Com
from ka_uts_com.log import Log

from typing import Any, List

T_Any = Any
T_Arr = List[Any]
T_Str = str

TN_Any = None | T_Any
TN_Str = None | T_Str


class Timestamp:

    @staticmethod
    def sh_elapse_time_sec(
            end: Any, start: TN_Any) -> TN_Any:
        if start is None:
            return None
        return end.timestamp()-start.timestamp()


class Timer:
    """ Timer Management
    """
    @staticmethod
    def sh_task_id(
            class_id: Any, parms: TN_Any, separator: T_Str) -> T_Str:
        """ start Timer
        """
        package = Com.pacmod_curr['package']
        module = Com.pacmod_curr['module']
        if isinstance(class_id, str):
            class_name = class_id
        else:
            class_name = class_id.__qualname__
        if not parms:
            parms = ""
        else:
            parms = f" {parms}"
        arr: T_Arr = []
        for item in [package, module, class_name, parms]:
            if not item:
                continue
            arr.append(item)
        return separator.join(arr)

    @classmethod
    def start(
            cls, class_id: T_Any,
            parms: TN_Any = None, separator: T_Str = ".") -> None:
        """ start Timer
        """
        task_id = cls.sh_task_id(class_id, parms, separator)
        Com.d_timer[task_id] = datetime.now()

    @classmethod
    def end(cls, class_id: T_Any,
            parms: TN_Any = None, separator: T_Str = ".") -> None:
        """ end Timer
        """
        task_id = cls.sh_task_id(class_id, parms, separator)
        start = Com.d_timer.get(task_id)
        end = datetime.now()
        elapse_time_sec = Timestamp.sh_elapse_time_sec(end, start)
        msg = f"{task_id} elapse time [sec] = {elapse_time_sec}"
        Log.info(msg, stacklevel=2)
