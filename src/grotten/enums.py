from __future__ import annotations

from enum import Enum
from gettext import gettext as _


class Direction(Enum):
    NORTH = _("north")
    EAST = _("east")
    SOUTH = _("south")
    WEST = _("west")

    def __neg__(self) -> Direction:
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }[self]
