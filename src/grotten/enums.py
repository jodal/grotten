from __future__ import annotations

from enum import Enum
from gettext import gettext as _


class Direction(str, Enum):
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


class Kind(str, Enum):
    ACTION = _("action")
    GAME = _("game")
    INVENTORY = _("inventory")
    ITEM = _("item")
    LEVEL = _("level")
    LIFE = _("life")
    LOCATION = _("location")
