from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional, Union

from moy_nalog.constants import CancelType
from moy_nalog.http import AuthDetails, HttpConnection
from moy_nalog.methods import (
    AddIncomeMethod,
    CancelIncomeMethod,
    UserMethod,
)
from moy_nalog.methods.api import BaseAPI
from moy_nalog.types import CanceledIncome, Credentials, Income, User


class MoyNalog:
    def __init__(
        self,
        login: str,
        password: str,
        timeout: float = 5.0,
        read_timeout: float = 5.0,
        write_timeout: float = 5.0,
        connect_timeout: float = 5.0,
    ) -> None:
        self.__login: str = login
        self.__password: str = password

        self._timeout: float = timeout
        self._read_timeout: float = read_timeout
        self._write_timeout: float = write_timeout
        self._connect_timeout: float = connect_timeout

        self._connection: HttpConnection = self._init_http()
        self._api: BaseAPI = self._init_api()

    @property
    def credentials(self) -> Credentials:
        return Credentials(self.__login, self.__password)

    @property
    def auth_details(self) -> Optional[AuthDetails]:
        return self._api.connection.auth.details

    def _init_http(self) -> HttpConnection:
        return HttpConnection(
            credentials=self.credentials,
            timeout=self._timeout,
            read_timeout=self._read_timeout,
            write_timeout=self._write_timeout,
            connect_timeout=self._connect_timeout,
        )

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
