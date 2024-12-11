from datetime import datetime
from datetime import timezone
from importlib.util import find_spec
from zoneinfo import ZoneInfo

if find_spec("django"):
    from django.conf import settings
else:
    settings = None

WSGI_BUFFER_INPUT_LIMIT = int(getattr(settings, "DATA_UPLOAD_MAX_MEMORY_SIZE", 25 * 1024 * 1024))
DRF_BEARER_TOKEN = getattr(settings, "BEARER_API_TOKEN", None)

UTC = timezone.utc

if hasattr(settings, "TIME_ZONE"):
    TIME_ZONE = ZoneInfo(settings.TIME_ZONE)
else:
    TIME_ZONE = datetime.now(UTC).astimezone().tzinfo

LOGGING_MIXIN_AUTH_INFO_FIELDS = getattr(settings, "LOGGER_AUTH_INFO_FIELDS", ("_auth",))
assert isinstance(LOGGING_MIXIN_AUTH_INFO_FIELDS, list | tuple), f"Expected {LOGGING_MIXIN_AUTH_INFO_FIELDS=!r} to be a list or tuple."
