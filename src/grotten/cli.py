from __future__ import annotations

from gettext import gettext as _
from typing import List, Optional, TYPE_CHECKING

import click
from click import secho as p

from grotten.actions import next_actions
from grotten.models import Game

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Item, Message


def main() -> None:
    game = Game.create()
    game.describe_location()

    try:
        while game.running and game.lives > 0:
            tick(game)
    except click.exceptions.Abort:
        banner(_("Aborting"))

    if game.running is False:
        banner(_("Welcome back"))
    if game.lives == 0:
        banner(_("Game over"))


def tick(game: Game) -> None:
    click.clear()
    show_messages(game.tick.messages)

    game.begin_tick()

    if game.tick.actions_allowed:
        action = select_action(next_actions(game))
        action.apply(game)

    if game.tick.inventory_open:
        show_inventory(game.inventory)


def show_messages(messages: List[Message]) -> None:
    for message in messages:
        describe(
            kind=message.kind, value=message.title, description=message.content
        )


def show_inventory(inventory: List[Item]) -> None:
    if not inventory:
        describe(kind=_("inventory"), value=_("empty"))

    for item in inventory:
        describe(kind=_("inventory"), value=item.name)

    click.pause(_("Press any key to close inventory ..."))


def select_action(actions: List[Action]) -> Action:
    p(_("What do you want to do?"), fg="blue")

    for i, action in enumerate(actions, 1):
        p(f"[{i}] ", nl=False, fg="yellow")
        p(str(action))

    num = click.prompt(
        click.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(actions)),
    )
    p()

    action = actions[num - 1]
    return action


def banner(text: str) -> None:
    p(f">>> {text} <<<", bold=True, fg="green")
    p()


def describe(
    *, kind: str, value: str, description: Optional[str] = None
) -> None:
    p(f"[{kind}] ", nl=False, fg="magenta")
    p(value, bold=description is not None)
    if description is not None:
        p(description)
    p()
