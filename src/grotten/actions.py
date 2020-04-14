from __future__ import annotations

from typing import List, TYPE_CHECKING

from dataclasses import dataclass

from grotten.enums import Direction
from grotten.i18n import _

if TYPE_CHECKING:
    from grotten.models import Game


@dataclass
class Action:
    def __str__(self) -> str:
        raise NotImplementedError

    def apply(self, game: Game) -> None:
        pass


@dataclass
class GoAction(Action):
    direction: Direction

    def __str__(self) -> str:
        return _(f"Go {self.direction.value}")

    def apply(self, game: Game) -> None:
        game.location = game.location.neighbors[self.direction]


@dataclass
class ExitAction(Action):
    def __str__(self) -> str:
        return _("Exit game")

    def apply(self, game: Game) -> None:
        game.end_game()


def next_actions(game: Game) -> List[Action]:
    actions: List[Action] = []
    for direction in Direction:
        if direction in game.location.neighbors:
            actions.append(GoAction(direction=direction))
    actions.append(ExitAction())
    return actions
