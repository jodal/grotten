from grotten.levels import get_level
from grotten.models import Level, Location


def test_get_level():
    level = get_level(1)

    assert isinstance(level, Level)
    assert level.number == 1
    assert isinstance(level.start, Location)
