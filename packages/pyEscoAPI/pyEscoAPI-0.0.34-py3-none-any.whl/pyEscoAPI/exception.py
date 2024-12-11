class PyEscoAPIError(Exception):
    def __init__(self, endpoint, status_code, error_message):
        self.endpoint = endpoint
        self.status_code = status_code
        self.error_message = error_message
