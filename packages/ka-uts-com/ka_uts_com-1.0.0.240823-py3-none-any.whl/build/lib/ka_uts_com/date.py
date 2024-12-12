from datetime import datetime
from datetime import date

T_Date = date
TN_Date = None | T_Date
TN_Str = None | str


class Date:

    @staticmethod
    def sh(datestring: TN_Str, fmt: str) -> TN_Date:
        if not datestring:
            return None
        return datetime.strptime(datestring, fmt).date()
