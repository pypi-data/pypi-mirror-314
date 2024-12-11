from typing import Union, Optional
import datetime

from moy_nalog.methods.api import BaseAPI


class BaseMethod:
    def __init__(self, api: BaseAPI) -> None:
        self._api = api

    def _format_date_to_local_iso(
        self,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
    ) -> str:
        if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
            date = date.replace(hour=23, minute=59, second=59).astimezone().isoformat()
        else:
            date = (
                datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
            )
        return date
