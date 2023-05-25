import json


class NeskError(Exception):
    pass


class HTTPError(NeskError):
    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason

    def __str__(self):
        return f"HTTP Error: {self.code} {self.reason}"


class URLError(NeskError):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return f"URL Error: {self.reason}"


class JSONDecodeError(NeskError):
    def __init__(self, error: json.JSONDecodeError):
        self.error = error

    def __str__(self):
        return f"JSONDecodeError: {self.error}"
