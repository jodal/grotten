from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _
from typing import Callable, Dict, List, Optional

from grotten import ui
from grotten.actions import next_actions
from grotten.enums import Direction
from grotten.levels import load_level


@dataclass(order=True)
class Item:
    name: str


@dataclass
class Location:
    name: str
    description: str = field(repr=False)
    neighbors: Dict[Direction, Location] = field(
        default_factory=dict, repr=False
    )
    items: List[Item] = field(default_factory=list, repr=False)
    effect: Optional[Callable[[Game], None]] = field(default=None, repr=False)

    def connect(self, direction: Direction, neighbor: Location) -> None:
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self

    def describe(self) -> None:
        ui.describe(
            kind=_("room"), value=self.name, description=self.description
        )
        for item in self.items:
            ui.describe(kind=_("item"), value=item.name)


@dataclass
class Level:
    number: int
    start: Location = field(repr=False)
    locations: Dict[str, Location] = field(default_factory=dict, repr=False)


@dataclass
class Game:
    level: Level
    location: Location
    lives: int = 3
    inventory: List[Item] = field(default_factory=list)

    game_done: bool = False
    tick_done: bool = False

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    def tick(self) -> None:
        self.tick_done = False

        self.location.describe()
        if self.location.effect is not None:
            self.location.effect(self)

        if self.tick_done:
            return

        action = ui.select_action(next_actions(self))
        action.apply(self)
        ui.clear()

    def end_game(self) -> None:
        self.game_done = True

    def lose_life(self) -> None:
        self.lives -= 1
        self.tick_done = self.lives == 0
        ui.describe(
            kind=_("life"),
            value=_("You lost a life."),
            description=_("You have {lives} left.").format(lives=self.lives),
        )

    def restart_level(self) -> None:
        self.location = self.level.start
        self.tick_done = True
        ui.describe(
            kind=_("level"),
            value=_("Restart"),
            description=_("You respawn at the beginning."),
        )

    def show_inventory(self) -> None:
        if not self.inventory:
            ui.describe(kind=_("inventory"), value=_("empty"))

        for item in self.inventory:
            ui.describe(kind=_("inventory"), value=item.name)

        ui.pause(_("Press any key to close inventory ..."))
