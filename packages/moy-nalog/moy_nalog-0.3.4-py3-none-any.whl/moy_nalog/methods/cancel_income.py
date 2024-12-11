from moy_nalog.methods.method import BaseMethod
from moy_nalog.methods.api import BaseAPI
from moy_nalog.constants import CancelType
from moy_nalog.types import CancellationInfo, CanceledIncome


class CancelIncomeMethod(BaseMethod):
    def __init__(
        self, api: BaseAPI, comment_type: CancelType, receipt_uuid: str
    ) -> None:
        super().__init__(api)

        self._comment_type = comment_type
        self._receipt_uuid = receipt_uuid

        self._BASE_URL = "/cancel"

    @property
    def body(self) -> dict:
        # operationTime and requestTime are same values
        time = self._format_date_to_local_iso()
        return {
            "comment": self._comment_type.value,
            "operationTime": time,
            "partnerCode": None,  # TODO: изучить, от чего зависит это значение
            "receiptUuid": self._receipt_uuid,
            "requestTime": time,
        }

    async def _make_request(self) -> dict:
        return await self._api.post(url=self._BASE_URL, json=self.body)

    async def execute(self):
        response = await self._make_request()
        income = response.get("incomeInfo")
        cancellation_info = income.get("cancellationInfo")

        return CanceledIncome(
            id=income.get("approvedReceiptUuid"),
            name=income.get("name"),
            operation_time=income.get("operationTime"),
            request_time=income.get("requestTime"),
            payment_type=income.get("paymentType"),  # TODO: make Enums
            partner_code=income.get("partnerCode"),  # TODO: learn this
            total_amount=income.get("totalAmount"),
            cancellation_info=CancellationInfo(
                operation_time=cancellation_info.get("operationTime"),
                register_time=cancellation_info.get("registerTime"),
                tax_period_id=cancellation_info.get("taxPeriodId"),
                comment=CancelType(value=cancellation_info.get("comment")),
            ),
            source_device_id=income.get("sourceDeviceId"),
        )
