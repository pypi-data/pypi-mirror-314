from moy_nalog.methods.method import BaseAPI, BaseMethod


class NotificationsMethod(BaseMethod):
    def __init__(self, api: BaseAPI) -> None:
        super().__init__(api)
