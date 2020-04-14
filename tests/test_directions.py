from grotten.models import Direction


def test_directions_are_ordered_clockwise():
    assert list(Direction) == [
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ]


def test_opposite_direction():
    assert -Direction.NORTH == Direction.SOUTH
    assert -Direction.EAST == Direction.WEST
    assert -Direction.SOUTH == Direction.NORTH
    assert -Direction.WEST == Direction.EAST
