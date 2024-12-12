class UnavailableServiceException(Exception):
    def __init__(self, message="Database unavailable", code="DatabaseUnavailable", exception_type="Database", status_code=503):
        self.message = message
        self.code = code
        self.type = exception_type
        self.status_code = status_code
        super().__init__(self.message)



