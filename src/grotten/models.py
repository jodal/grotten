from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

from grotten import ui
from grotten.actions import next_actions
from grotten.enums import Direction
from grotten.i18n import _
from grotten.levels import get_level


@dataclass
class Location:
    name: str
    description: str = field(repr=False)
    neighbors: Dict[Direction, Location] = field(
        default_factory=dict, repr=False
    )
    effect: Optional[Callable[[Game], None]] = field(default=None, repr=False)

    def connect(self, direction: Direction, neighbor: Location) -> None:
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self

    def describe(self) -> None:
        ui.describe(
            kind=_("room"), value=self.name, description=self.description
        )


@dataclass
class Level:
    number: int
    start: Location = field(repr=False)


@dataclass
class Game:
    level: Level
    location: Location
    lives: int = 3

    game_done: bool = False
    tick_done: bool = False

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = get_level(1)
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
            description=_(f"You have {self.lives} left."),
        )

    def restart_level(self) -> None:
        self.location = self.level.start
        self.tick_done = True
        ui.describe(
            kind=_("level"),
            value=_("Restart"),
            description=_("You respawn at the beginning."),
        )
