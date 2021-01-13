class Bbb2Error(Exception):
    def __init__(self, message):
        super().__init__(message)

class ApiParseError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class BadRequestError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class ConnectError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class ExpiredAuthError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class InternalError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class RemoteError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class RemoteResourceLimitError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)

class UnauthorizedError(Bbb2Error):
    def __init__(self, message):
        super().__init__(message)
