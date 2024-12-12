class InvalidModelError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidModelJobError(Exception):
    def __init__(self, message):
        super().__init__(message)