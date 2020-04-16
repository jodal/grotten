from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _
from typing import Callable, Dict, List, Optional

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


@dataclass
class Level:
    number: int
    start: Location = field(repr=False)
    locations: Dict[str, Location] = field(default_factory=dict, repr=False)


@dataclass
class Message:
    kind: str
    title: str
    content: Optional[str]


@dataclass
class Tick:
    messages: List[Message] = field(default_factory=list)
    inventory_open: bool = False
    actions_allowed: bool = True


@dataclass
class Game:
    level: Level
    location: Location
    inventory: List[Item] = field(default_factory=list)
    lives: int = 3
    running: bool = True
    tick: Tick = field(default_factory=Tick)

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    def end_game(self) -> None:
        self.running = False

    def begin_tick(self) -> None:
        self.tick = Tick()

    def create_message(
        self, *, kind: str, title: str, content: Optional[str] = None
    ) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.tick.messages.append(message)
        return message

    def die(self) -> None:
        self.lives -= 1
        self.tick.actions_allowed = self.lives > 0
        self.create_message(
            kind=_("life"),
            title=_("You died"),
            content=_("You have {lives} left.").format(lives=self.lives),
        )

    def restart_level(self) -> None:
        self.location = self.level.start
        self.tick.actions_allowed = False
        self.create_message(
            kind=_("level"),
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )

    def show_inventory(self) -> None:
        self.tick.inventory_open = True
