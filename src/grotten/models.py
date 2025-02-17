from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from grotten.actions import Action
    from grotten.enums import Direction, Kind
    from grotten.game import Game


@dataclass(order=True)
class Creature:
    name: str
    strength: int = 1
    loot: list[Item] = field(default_factory=list)


@dataclass(order=True)
class Item:
    name: str
    attack_strength: int = 0


@dataclass
class Location:
    name: str
    description: str = field(repr=False)
    neighbors: dict[Direction, Location] = field(default_factory=dict, repr=False)
    actions: list[Action] = field(default_factory=list, repr=False)
    creatures: list[Creature] = field(default_factory=list, repr=False)
    items: list[Item] = field(default_factory=list, repr=False)
    effect: Callable[[Game], None] | None = field(default=None, repr=False)

    def connect(self, direction: Direction, neighbor: Location) -> None:
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self


@dataclass
class Level:
    number: int
    name: str
    start: Location = field(repr=False)
    locations: dict[str, Location] = field(default_factory=dict, repr=False)


@dataclass
class Inventory:
    items: list[Item] = field(default_factory=list)

    def add(self, item: Item) -> None:
        self.items = sorted([*self.items, item])

    def get_weapon(self) -> Item:
        best_weapon = Item(_("Bare Hands"), attack_strength=3)
        for item in self.items:
            if item.attack_strength > best_weapon.attack_strength:
                best_weapon = item
        return best_weapon


@dataclass
class Message:
    kind: Kind
    title: str
    content: str | None = None


@dataclass
class Mailbox:
    messages: list[Message] = field(default_factory=list)

    def add(self, *, kind: Kind, title: str, content: str | None = None) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.messages.append(message)
        return message

    def pop(self) -> list[Message]:
        messages, self.messages = self.messages, []
        return messages

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index: int) -> Message:
        return self.messages[index]
