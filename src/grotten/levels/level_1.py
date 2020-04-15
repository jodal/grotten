from grotten.i18n import _
from grotten.enums import Direction
from grotten.models import Game, Level, Location


# Effects
def fall_into_pit(game: Game) -> None:
    game.lose_life()
    if game.lives > 0:
        game.restart_level()


# Locations
entrance = Location(
    name=_("Entrance"),
    description=_("You find yourself in a dark and scary cave."),
)
pit = Location(
    name=_("Pit"),
    description=_("You fell into a deep dark pit."),
    effect=fall_into_pit,
)
dragon_lair = Location(
    name=_("Dragon lair"),
    description=_(
        "There is large green dragon sleeping on the floor in front of you."
    ),
)
skeletons = Location(
    name=_("Skeletons"),
    description=_("You stumble upon the skeletons of three humans and a dog."),
)
treasure = Location(
    name=_("Treasure"), description=_("You found the treasure!"),
)


# Connections
entrance.connect(Direction.NORTH, pit)
entrance.connect(Direction.WEST, dragon_lair)
dragon_lair.connect(Direction.NORTH, skeletons)
skeletons.connect(Direction.NORTH, treasure)


# Level
level = Level(
    number=1,
    start=entrance,
    locations={
        "entrance": entrance,
        "pit": pit,
        "skeletons": skeletons,
        "dragon_lair": dragon_lair,
        "treasure": treasure,
    },
)
