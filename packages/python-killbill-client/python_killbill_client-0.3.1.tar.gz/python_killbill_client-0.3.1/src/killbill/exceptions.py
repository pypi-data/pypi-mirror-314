class KillBillError(Exception):
    """Raised when the Kill Bill API returns an error"""

    def __init__(self, msg: object) -> None:
        super().__init__(msg)


class UnknownError(KillBillError):
    def __init__(self, msg: object = "Unknown Error") -> None:
        super().__init__(msg)


class AuthError(Exception):
    def __init__(self, msg: object = "Unauthorized") -> None:
        super().__init__(msg)


class NotFoundError(Exception):
    def __init__(self, msg: object = "Source Not Found") -> None:
        super().__init__(msg)
