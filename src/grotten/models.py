from __future__ import annotations

from dataclasses import dataclass, field
from gettext import gettext as _, ngettext
from typing import Callable, Dict, List, Optional

from grotten import actions
from grotten.enums import Direction, Kind
from grotten.levels import load_level


@dataclass(order=True)
class Creature:
    name: str


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
    creatures: List[Creature] = field(default_factory=list, repr=False)
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
    kind: Kind
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

    def create_message(
        self, *, kind: Kind, title: str, content: Optional[str] = None
    ) -> Message:
        message = Message(kind=kind, title=title, content=content)
        self.messages.append(message)
        return message

    def pop_messages(self) -> List[Message]:
        messages = self.messages
        self.messages = []
        return messages

    # --- Actions

    def available_actions(self) -> List[actions.Action]:
        result: List[actions.Action] = []

        for item in self.location.items:
            result.append(actions.PickUp(item=item))

        for direction in Direction:
            if direction in self.location.neighbors:
                result.append(actions.Go(direction=direction))

        result.append(actions.ShowInventory())
        result.append(actions.EndGame())

        return result

    def apply(self, action: actions.Action) -> None:
        if isinstance(action, actions.EndGame):
            return self.end_game()
        if isinstance(action, actions.Go):
            return self.go(action.direction)
        if isinstance(action, actions.PickUp):
            return self.pick_up(action.item)
        if isinstance(action, actions.ShowInventory):
            return self.show_inventory()

    def end_game(self) -> None:
        self.running = False
        self.create_message(kind=Kind.GAME, title=_("Welcome back"))

    def go(self, direction: Direction) -> None:
        self.location = self.location.neighbors[direction]
        self.create_message(
            kind=Kind.ACTION,
            title=_("Going {direction}").format(direction=_(direction)),
        )
        self.describe_location()
        if self.location.effect is not None:
            self.location.effect(self)

    def pick_up(self, item: Item) -> None:
        self.location.items.remove(item)
        self.inventory = sorted(self.inventory + [item])
        self.create_message(
            kind=Kind.ACTION,
            title=_("Picking up {item}").format(item=item.name),
        )

    def show_inventory(self) -> None:
        if not self.inventory:
            self.create_message(
                kind=Kind.INVENTORY,
                title=_("empty"),
                content=_("The inventory is empty."),
            )

        for item in self.inventory:
            self.create_message(kind=Kind.INVENTORY, title=item.name)

    # --- Action building blocks

    def describe_location(self) -> None:
        self.create_message(
            kind=Kind.LOCATION,
            title=self.location.name,
            content=self.location.description,
        )

        for creature in self.location.creatures:
            self.create_message(kind=Kind.CREATURE, title=creature.name)

        for item in self.location.items:
            self.create_message(kind=Kind.ITEM, title=item.name)

    def die(self) -> None:
        self.lives -= 1
        self.create_message(
            kind=Kind.LIFE,
            title=_("You died"),
            content=ngettext(
                _("You have only {lives} life left."),
                _("You have {lives} lives left."),
                self.lives,
            ).format(lives=self.lives),
        )
        if self.lives == 0:
            self.create_message(kind=Kind.GAME, title=_("Game over"))

    def restart_level(self) -> None:
        self.location = self.level.start
        self.create_message(
            kind=Kind.LEVEL,
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )
