from __future__ import annotations

from gettext import gettext as _
from typing import TYPE_CHECKING

from grotten.actions import CustomAction, Effect
from grotten.enums import Direction
from grotten.models import Creature, Item, Level, Location

if TYPE_CHECKING:
    from grotten.game import Game


# Effects
def teleport(to: Location) -> Effect:
    def effect(game: Game) -> None:
        game.location = to

    return effect


# Locations
bedroom = Location(
    name=_("Bedroom"),
    description=_("You're in an dusty bedroom with stone walls."),
)
weaponry = Location(
    name=_("Weaponry"),
    description=_("This looks like a looted and abandoned weaponry."),
    items=[
        Item(name=_("Wooden Bow"), attack_strength=10),
        Item(name=_("Arrow")),
        Item(name=_("Arrow")),
    ],
)
hallway = Location(
    name=_("Hallway"),
    description=_("A long hallway of badly lit portraits of old grumpy men."),
)
bird_cages = Location(
    name=_("Bird cages"),
    description=_(
        "There is a number of gigantic bird cages along the stone wall. "
        "All of them are empty, some with the door unhinged."
    ),
    creatures=[
        Creature(name=_("Giant Moa"), strength=8),
        Creature(name=_("Spotted Kiwi"), strength=2),
        Creature(name=_("Ostrich"), strength=5),
    ],
)
portal = Location(
    name=_("Portal room"),
    description=_(
        "The hallway widens into a large room. "
        "In the middle there is a strange mirror with a surface that seems to wobble."
    ),
    actions=[
        CustomAction(
            description=_("Touch the wobbling mirror"),
            effect=teleport(to=bird_cages),
        ),
    ],
)
treasure = Location(
    name=_("Treasure"),
    description=_("You found the treasure!"),
)

# Connections
bedroom.connect(Direction.EAST, weaponry)
bedroom.connect(Direction.WEST, hallway)
hallway.connect(Direction.NORTH, portal)
bird_cages.connect(Direction.EAST, treasure)


# Level
level = Level(
    number=2,
    name=_("Bird cages"),
    start=bedroom,
    locations={
        "bedroom": bedroom,
        "weaponry": weaponry,
        "hallway": hallway,
        "portal": portal,
        "bird_cages": bird_cages,
        "treasure": treasure,
    },
)
