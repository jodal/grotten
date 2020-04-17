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
class Game:
    level: Level
    location: Location
    inventory: List[Item] = field(default_factory=list)
    lives: int = 3
    running: bool = True
    messages: List[Message] = field(default_factory=list)

    @classmethod
    def create(cls, *, level: Optional[Level] = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    def end_game(self) -> None:
        self.running = False

    def pop_messages(self) -> List[Message]:
        messages = self.messages
        self.messages = []
        return messages

    def create_message(
        self, *, kind: str, title: str, content: Optional[str] = None
    ) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.messages.append(message)
        return message

    def go(self, direction: Direction) -> None:
        self.location = self.location.neighbors[direction]
        self.create_message(
            kind=_("action"),
            title=_("Going {direction}").format(direction=_(direction.value)),
        )
        self.describe_location()
        if self.location.effect is not None:
            self.location.effect(self)

    def describe_location(self) -> None:
        self.create_message(
            kind=_("location"),
            title=self.location.name,
            content=self.location.description,
        )
        for item in self.location.items:
            self.create_message(kind=_("item"), title=item.name)

    def die(self) -> None:
        self.lives -= 1
        self.create_message(
            kind=_("life"),
            title=_("You died"),
            content=_("You have {lives} left.").format(lives=self.lives),
        )

    def restart_level(self) -> None:
        self.location = self.level.start
        self.create_message(
            kind=_("level"),
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )

    def pick_up(self, item: Item) -> None:
        self.location.items.remove(item)
        self.inventory = sorted(self.inventory + [item])
        self.create_message(
            kind=_("action"),
            title=_("Picking up {item}").format(item=item.name),
        )

    def show_inventory(self) -> None:
        if not self.inventory:
            self.create_message(
                kind=_("inventory"),
                title=_("empty"),
                content=_("The inventory is empty."),
            )

        for item in self.inventory:
            self.create_message(kind=_("inventory"), title=item.name)
