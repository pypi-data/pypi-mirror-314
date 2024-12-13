from moy_nalog.methods.method import BaseAPI, BaseMethod


class BonusMethod(BaseMethod):
    def __init__(self, api: BaseAPI):
        super().__init__(api)
