import pytest

from .consts import REGISTRATION_NUMBER_RE

ROMANIAN_REGISTRATION_NUMBER_RE = REGISTRATION_NUMBER_RE["RO"]


@pytest.mark.parametrize(
    ("registration_number", "match"),
    [
        ("B03LRW", True),
        ("B100ABC", True),
        ("B010ABC", False),
        ("B001ABC", False),
        ("B01ABC", True),
        ("B00ABC", False),
        ("MM01ABC", True),
        ("MM00ABC", False),
    ],
)
def test_registration_number_re_ro(registration_number, match):
    assert bool(ROMANIAN_REGISTRATION_NUMBER_RE.match(registration_number)) == match, f"{registration_number} expected {match} match"
