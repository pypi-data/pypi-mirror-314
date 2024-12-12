# coding=utf-8

from ka_uts_com.pacmod import Pacmod
from ka_uts_com.aeq import Aeq

from typing import Any, Callable, Dict, List

T_Arr = List[Any]
T_Dic = Dict[Any, Any]

TN_Arr = None | T_Arr
TN_Dic = None | T_Dic


class Argv:
    """ Manage Commandline Arguments
    """
    @staticmethod
    def set_by_pacmod(d_eq: T_Dic, root_cls) -> None:
        """ set current pacmod dictionary
        """
        tenant = d_eq.get('tenant')
        d_eq['pacmod_curr'] = Pacmod.sh_d_pacmod(root_cls, tenant)

    @staticmethod
    def set_by_prof(d_eq: T_Dic, sh_prof: Callable | Any) -> None:
        """ set current pacmod dictionary
        """
        if callable(sh_prof):
            d_eq['sh_prof'] = sh_prof()
        else:
            d_eq['sh_prof'] = sh_prof

    @classmethod
    def sh(cls, a_s_eq: T_Arr, **kwargs) -> T_Dic:
        """ show equates dictionary
        """
        # print(f"DoEq sh kwargs = {kwargs}")
        root_cls = kwargs.get('root_cls')
        d_valid_parms: TN_Dic = kwargs.get('d_parms')
        # print(f"DoEq sh d_valid_parms = {d_valid_parms}")

        d_eq = Aeq.sh_d_eq(a_s_eq, d_valid_parms)

        cls.set_by_pacmod(d_eq, root_cls)
        _sh_prof = kwargs.get('sh_prof')
        cls.set_by_prof(d_eq, _sh_prof)

        return d_eq
