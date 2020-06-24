from __future__ import annotations

from dataclasses import dataclass
from gettext import gettext as _
from typing import TYPE_CHECKING

from grotten.enums import Direction

if TYPE_CHECKING:
    from grotten.models import Creature, Item


@dataclass
class Action:
    def __str__(self) -> str:
        raise NotImplementedError

    def is_meta_action(self) -> bool:
        return False

    def apply(self, game: Game) -> None:
        raise NotImplementedError


@dataclass
class EndGame(Action):
    def __str__(self) -> str:
        return _("End game")

    def is_meta_action(self) -> bool:
        return True

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
class Attack(Action):
    creature: Creature

    def __str__(self) -> str:
        return _("Attack {creature}").format(creature=self.creature.name)

    def apply(self, game: Game) -> None:
        game.attack(self.creature)


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

    def is_meta_action(self) -> bool:
        return True

    def apply(self, game: Game) -> None:
        game.show_inventory()
