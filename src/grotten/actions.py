from __future__ import annotations

from dataclasses import dataclass
from gettext import gettext as _
from typing import TYPE_CHECKING, Protocol

from grotten.enums import Direction

if TYPE_CHECKING:
    from grotten.game import Game
    from grotten.models import Creature, Item


class Effect(Protocol):
    def __call__(self, game: Game) -> None:
        pass


@dataclass
class Action:
    def __str__(self) -> str:
        raise NotImplementedError

    def is_meta_action(self) -> bool:
        return False

    def apply(self, game: Game) -> None:
        raise NotImplementedError


@dataclass
class CustomAction(Action):
    description: str
    effect: Effect

    def __str__(self) -> str:
        return self.description

    def apply(self, game: Game) -> None:
        self.effect(game)


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


# --- Meta actions


@dataclass
class MetaAction(Action):
    def is_meta_action(self) -> bool:
        return True


@dataclass
class EndGame(MetaAction):
    def __str__(self) -> str:
        return _("End game")

    def apply(self, game: Game) -> None:
        game.end_game()


@dataclass
class ShowInventory(MetaAction):
    def __str__(self) -> str:
        return _("Show inventory")

    def apply(self, game: Game) -> None:
        game.show_inventory()
