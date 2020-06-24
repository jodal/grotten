from __future__ import annotations

from gettext import gettext as _
from typing import List, TYPE_CHECKING

import click

from grotten import __version__
from grotten.game import Game
from grotten.levels import load_level

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Message


@click.command()
@click.option("-l", "--level", default=1, help="Level to start at.")
@click.version_option(version=__version__)
def main(level: int) -> None:
    game = Game.create(level=load_level(level))
    game.describe_location()

    try:
        while game.running and game.lives > 0:
            click.clear()
            show_messages(game.messages.pop())
            action = select_action(game.available_actions())
            action.apply(game)
    except click.exceptions.Abort:
        click.echo()
        click.secho(_("Aborting"), bold=True, fg="yellow")

    click.clear()
    show_messages(game.messages.pop())


def show_messages(messages: List[Message]) -> None:
    for message in messages:
        click.secho(f"[{_(message.kind)}] ", nl=False, fg="magenta")
        click.secho(message.title, bold=True)
        if message.content is not None:
            click.secho(message.content)
        click.echo()


def select_action(actions: List[Action]) -> Action:
    click.secho(_("What do you want to do?"), fg="blue")

    for i, action in enumerate(actions, 1):
        click.secho(f"[{i}] ", nl=False, fg="yellow")
        click.secho(
            str(action), fg="white" if action.is_meta_action() else None
        )

    num = click.prompt(
        click.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(actions)),
    )
    click.echo()

    action = actions[num - 1]
    return action
