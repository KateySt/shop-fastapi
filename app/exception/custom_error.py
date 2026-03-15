class CustomError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class ValidationError(CustomError):
    pass


class NotFoundError(CustomError):
    pass


class AlreadyExistsError(CustomError):
    pass
