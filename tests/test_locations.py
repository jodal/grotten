import pytest

from grotten.enums import Direction
from grotten.models import Location


@pytest.fixture
def bedroom():
    return Location(name="Bedroom", description="Dusty master bedroom")


@pytest.fixture
def bathroom():
    return Location(name="Bathroom", description="Tiny and dirty bathroom")


def test_new_room(bedroom):
    assert bedroom.name == "Bedroom"
    assert bedroom.description == "Dusty master bedroom"
    assert bedroom.neighbors == {}


def test_connect(bedroom, bathroom):
    bedroom.connect(Direction.NORTH, bathroom)

    assert bedroom.neighbors == {Direction.NORTH: bathroom}
    assert bathroom.neighbors == {Direction.SOUTH: bedroom}
