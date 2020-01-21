class BackblazeB2Error(Exception):
    def __init__(self, message):
        super().__init__(message)

class BackblazeB2BadRequestError(BackblazeB2Error):
    def __init__(self, message):
        super().__init__(message)

class BackblazeB2ConnectError(BackblazeB2Error):
    def __init__(self, message):
        super().__init__(message)

class BackblazeB2ExpiredAuthError(BackblazeB2Error):
    def __init__(self, message):
        super().__init__(message)
