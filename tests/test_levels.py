from grotten.levels import load_level
from grotten.models import Level, Location


def test_load_level():
    level = load_level(1)

    assert isinstance(level, Level)
    assert level.number == 1
    assert isinstance(level.start, Location)

    other = load_level(1)

    assert level is not other
