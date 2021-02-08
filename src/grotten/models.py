from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from grotten.enums import Direction, Kind

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.game import Game


@dataclass(order=True)
class Creature:
    name: str
    strength: int = 1
    loot: List[Item] = field(default_factory=list)


@dataclass(order=True)
class Item:
    name: str
    attack_strength: int = 0


@dataclass
class Location:
    name: str
    description: str = field(repr=False)
    neighbors: Dict[Direction, Location] = field(
        default_factory=dict, repr=False
    )
    actions: List[Action] = field(default_factory=list, repr=False)
    creatures: List[Creature] = field(default_factory=list, repr=False)
    items: List[Item] = field(default_factory=list, repr=False)
    effect: Optional[Callable[[Game], None]] = field(default=None, repr=False)

    def connect(self, direction: Direction, neighbor: Location) -> None:
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self


@dataclass
class Level:
    number: int
    name: str
    start: Location = field(repr=False)
    locations: Dict[str, Location] = field(default_factory=dict, repr=False)


@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)

    def add(self, item: Item) -> None:
        self.items = sorted(self.items + [item])

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
    content: Optional[str] = None


@dataclass
class Mailbox:
    messages: List[Message] = field(default_factory=list)

    def add(
        self, *, kind: Kind, title: str, content: Optional[str] = None
    ) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.messages.append(message)
        return message

    def pop(self) -> List[Message]:
        messages, self.messages = self.messages, []
        return messages

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index: int) -> Message:
        return self.messages[index]
