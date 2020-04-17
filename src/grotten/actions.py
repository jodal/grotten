from __future__ import annotations

from dataclasses import dataclass
from gettext import gettext as _
from typing import List, TYPE_CHECKING

from grotten.enums import Direction

if TYPE_CHECKING:
    from grotten.models import Game, Item


@dataclass
class Action:
    def __str__(self) -> str:
        raise NotImplementedError

    def apply(self, game: Game) -> None:
        pass


@dataclass
class EndGame(Action):
    def __str__(self) -> str:
        return _("End game")

    def apply(self, game: Game) -> None:
        game.end_game()


@dataclass
class Go(Action):
    direction: Direction

    def __str__(self) -> str:
        return _("Go {direction}").format(direction=_(self.direction.value))

    def apply(self, game: Game) -> None:
        game.go(self.direction)


@dataclass
class PickUp(Action):
    item: Item

    def __str__(self) -> str:
        return _("Pick up {item}").format(item=self.item.name)

    def apply(self, game: Game) -> None:
        game.pick_up(self.item)


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
    actions.append(EndGame())

    return actions
