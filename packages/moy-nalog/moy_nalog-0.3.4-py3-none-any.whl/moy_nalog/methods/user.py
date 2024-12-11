from typing import Optional
from datetime import datetime

from moy_nalog.methods.method import BaseMethod
from moy_nalog.methods.api import BaseAPI
from moy_nalog.types import User


class UserMethod(BaseMethod):
    def __init__(self, api: BaseAPI) -> None:
        super().__init__(api)

        self._BASE_URL = "/user"

    @staticmethod
    def iso_date_to_datetime(iso_date: Optional[str]) -> Optional[datetime]:
        if not iso_date:
            return
        return datetime.fromisoformat(iso_date[:-1] + "+00:00")

    async def _make_request(self) -> dict:
        return await self._api.get(self._BASE_URL)

    async def execute(self) -> User:
        response = await self._make_request()

        initial_registration_date = response.get("initialRegistrationDate")
        registration_date = response.get("registrationDate")
        first_receipt_register_time = response.get("firstReceiptRegisterTime")
        first_receipt_cancel_time = response.get("firstReceiptCancelTime")

        return User(
            last_name=response.get("lastName"),
            id=response.get("id"),
            display_name=response.get("displayName"),
            middle_name=response.get("middleName"),
            email=response.get("email"),
            phone=response.get("phone"),
            inn=response.get("inn"),
            snils=response.get("snils"),
            avatar_exists=response.get("avatarExists"),
            initial_registration_date=self.iso_date_to_datetime(
                initial_registration_date
            ),
            registration_date=self.iso_date_to_datetime(registration_date),
            first_receipt_register_time=self.iso_date_to_datetime(
                first_receipt_register_time
            ),
            first_receipt_cancel_time=self.iso_date_to_datetime(
                first_receipt_cancel_time
            ),
            hide_cancelled_receipt=response.get("hideCancelledReceipt"),
            register_available=response.get("registerAvailable"),
            status=response.get("status"),
            restricted_mode=response.get("restrictedMode"),
            pfr_url=response.get("pfrUrl"),
            login=response.get("login"),
        )
