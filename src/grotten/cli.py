from __future__ import annotations

from gettext import gettext as _
from typing import List, TYPE_CHECKING

import click
from click import secho as p

from grotten.actions import next_actions
from grotten.models import Game

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Message


def main() -> None:
    game = Game.create()
    game.describe_location()

    try:
        while game.running and game.lives > 0:
            tick(game)
    except click.exceptions.Abort:
        p()
        p(_("Aborting"), bold=True, fg="yellow")

    if game.running is False:
        p(_("Welcome back"), bold=True)
    if game.lives == 0:
        p(_("Game over"), bold=True, fg="red")


def tick(game: Game) -> None:
    click.clear()

    show_messages(game.pop_messages())

    action = select_action(next_actions(game))
    action.apply(game)


def show_messages(messages: List[Message]) -> None:
    for message in messages:
        p(f"[{message.kind}] ", nl=False, fg="magenta")
        p(message.title, bold=True)
        if message.content is not None:
            p(message.content)
        p()


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
