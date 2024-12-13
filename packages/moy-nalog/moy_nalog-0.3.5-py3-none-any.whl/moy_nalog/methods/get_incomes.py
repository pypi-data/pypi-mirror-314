from datetime import datetime

from moy_nalog.constants import HistorySortBy
from moy_nalog.methods.method import BaseAPI, BaseMethod


class GetIncomesMethod(BaseMethod):
    def __init__(
        self,
        api: BaseAPI,
        from_: datetime,
        to: datetime,
        offset,
        sort_by: HistorySortBy,
        limit: int = 10,
    ) -> None:
        super().__init__(api)

        # from = ISO datetime (2024-11-01T00:00:00.562+05:00)
        # to = ISO datetime (2024-12-10T23:59:59.562+05:00)
        # offset = int (0)
        # sortBy = param (operation_time):desc
        # limit= int (10)
