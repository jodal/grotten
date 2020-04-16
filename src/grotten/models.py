from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _
from typing import Callable, Dict, List, Optional

from grotten.enums import Direction
from grotten.levels import load_level


@dataclass
class Message:
    kind: str
    title: str
    content: Optional[str]


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


@dataclass
class Level:
    number: int
    start: Location = field(repr=False)
    locations: Dict[str, Location] = field(default_factory=dict, repr=False)


@dataclass
class Game:
    level: Level
    location: Location
    running: bool = True
    lives: int = 3
    inventory: List[Item] = field(default_factory=list)

    # Tick state
    messages: List[Message] = field(default_factory=list)
    inventory_open: bool = False
    actions_allowed: bool = True

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    def tick_reset(self) -> None:
        self.messages = []
        self.inventory_open = False
        self.actions_allowed = True

    def message(
        self, *, kind: str, title: str, content: Optional[str] = None
    ) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.messages.append(message)
        return message

    def end_game(self) -> None:
        self.running = False

    def lose_life(self) -> None:
        self.lives -= 1
        self.actions_allowed = self.lives > 0
        self.message(
            kind=_("life"),
            title=_("You lost a life."),
            content=_("You have {lives} left.").format(lives=self.lives),
        )

    def restart_level(self) -> None:
        self.location = self.level.start
        self.actions_allowed = False
        self.message(
            kind=_("level"),
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )

    def show_inventory(self) -> None:
        self.inventory_open = True
