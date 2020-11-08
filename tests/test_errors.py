class TestError(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadMockRequestError(TestError):
    def __init__(self, message):
        super().__init__(message)
