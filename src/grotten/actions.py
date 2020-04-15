from __future__ import annotations

from typing import List, TYPE_CHECKING

from dataclasses import dataclass

from grotten.enums import Direction
from grotten.i18n import _

if TYPE_CHECKING:
    from grotten.models import Game, Item


@dataclass
class Action:
    def __str__(self) -> str:
        raise NotImplementedError

    def apply(self, game: Game) -> None:
        pass


@dataclass
class Exit(Action):
    def __str__(self) -> str:
        return _("Exit game")

    def apply(self, game: Game) -> None:
        game.end_game()


@dataclass
class Go(Action):
    direction: Direction

    def __str__(self) -> str:
        return _(f"Go {self.direction.value}")

    def apply(self, game: Game) -> None:
        game.location = game.location.neighbors[self.direction]


@dataclass
class PickUp(Action):
    item: Item

    def __str__(self) -> str:
        return _(f"Pick up {self.item.name}")

    def apply(self, game: Game) -> None:
        game.location.items.remove(self.item)
        game.inventory.append(self.item)
        game.inventory = sorted(game.inventory)


@dataclass
class ShowInventory(Action):
    def __str__(self) -> str:
        return _("Show inventory")

    def apply(self, game: Game) -> None:
        game.show_inventory()


def next_actions(game: Game) -> List[Action]:
    actions: List[Action] = []

    for item in game.location.items:
        actions.append(PickUp(item=item))

    for direction in Direction:
        if direction in game.location.neighbors:
            actions.append(Go(direction=direction))

    actions.append(ShowInventory())
    actions.append(Exit())

    return actions
