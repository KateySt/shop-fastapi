class ValidationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)
