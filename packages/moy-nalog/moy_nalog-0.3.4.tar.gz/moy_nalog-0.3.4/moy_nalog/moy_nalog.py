from __future__ import annotations

from typing import Any, Optional, Union
from datetime import datetime, date

from moy_nalog.methods import (
    AddIncomeMethod,
    CancelIncomeMethod,
    UserMethod,
)
from moy_nalog.methods.api import BaseAPI
from moy_nalog.http import HttpConnection, AuthDetails
from moy_nalog.constants import CancelType
from moy_nalog.types import Credentials, Income, CanceledIncome, User


class MoyNalog:
    def __init__(self, login: str, password: str) -> None:
        self.__login = login
        self.__password = password

        self._connection: HttpConnection = self._init_http()
        self._api: BaseAPI = self._init_api()

    @property
    def credentials(self) -> Credentials:
        return Credentials(self.__login, self.__password)

    @property
    def auth_details(self) -> Optional[AuthDetails]:
        return self._api.connection.auth.details

    def _init_http(self) -> HttpConnection:
        return HttpConnection(self.credentials)

    def _init_api(self) -> BaseAPI:
        return BaseAPI(self._connection)

    async def add_income(
        self,
        name: str,
        created_at: Union[datetime, date],
        quantity: int,
        amount: Union[int, float],
    ) -> Income:
        return await AddIncomeMethod(
            api=self._api,
            name=name,
            created_at=created_at,
            quantity=quantity,
            amount=amount,
        ).execute()

    async def cancel_income(
        self, receipt_uuid: str, comment_type: CancelType
    ) -> CanceledIncome:
        return await CancelIncomeMethod(
            api=self._api, comment_type=comment_type, receipt_uuid=receipt_uuid
        ).execute()

    async def get_user_info(self) -> User:
        return await UserMethod(api=self._api).execute()

    async def __aenter__(self) -> MoyNalog:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._connection.close()

    async def close(self) -> None:
        await self._connection.close()

    def __repr__(self) -> str:
        return "MoyNalog()"

    def __hash__(self) -> int:
        return hash(f"{self.credentials.username}:{self.credentials.password}")

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, MoyNalog):
            return False
        return hash(self) == hash(value)
