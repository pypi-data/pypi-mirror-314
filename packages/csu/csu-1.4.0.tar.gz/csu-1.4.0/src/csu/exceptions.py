from collections.abc import Iterable
from os import urandom

from .timezones import naivenow

try:
    from rest_framework.exceptions import APIException
    from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
except ImportError:

    class APIException(Exception):
        pass

    HTTP_503_SERVICE_UNAVAILABLE = 503


def get_accident_id():
    dt = naivenow()
    d = dt.date()
    t = dt.timestamp() % 86400
    return f"{d.year:2}{d.month:02}{d.day:02}:{urandom(4).hex()}:{t:08.2f}"


class TaggedError(Exception):
    def __init__(self, *details, event_id):
        super().__init__(*details)
        self.event_id = event_id

    def __str__(self):
        return f'{type(self).__name__}({", ".join(map(str, self.args))})'

    def __repr__(self):
        args = [repr(arg) for arg in self.args]
        args.append(f"event_id={self.event_id}")
        return f'{type(self).__name__}({", ".join(args)})'


class RetryableError(TaggedError):
    """
    Either the service is down or temporarily broken (eg: 404/5xx states, malformed responses etc). Retryable.
    """


class HTTPErrorMixin:
    status_code: int

    def __init__(self, status_code, *args, event_id):
        super().__init__(status_code, *args, event_id=event_id)
        self.status_code = status_code


class DecodingError(HTTPErrorMixin, RetryableError):
    """
    When content decoding fails.
    """


class InternalServiceError(TaggedError):
    """
    The service failed in handling (expected fields are missing, buggy code etc). Not retryable.
    """


class UnexpectedStatusError(HTTPErrorMixin, InternalServiceError):
    """
    When response status is bad.
    """


class ExhaustedRetriesError(InternalServiceError):
    """
    The service reached the retry limit. Obviously not retryable.
    """


class OpenServiceError(TaggedError):
    """
    The service failed in handling in a way that should be propagated upward the public API.
    """

    default_message: object
    code: str = "unknown"

    def __init__(self, message=None, *, details: Iterable = (), event_id):
        super().__init__(*details, event_id=event_id)
        self.message = str(message or self.default_message)


class APIServiceError(APIException):
    status_code = HTTP_503_SERVICE_UNAVAILABLE

    def __init__(self, message, *, code="unavailable", event_id=None, **kwargs):
        self.message = message
        self.detail = {
            "accident_id": get_accident_id() if event_id is None else event_id,
            "detail": message,
            "code": code,
            **kwargs,
        }
