from __future__ import annotations

from gettext import gettext as _
from typing import List, TYPE_CHECKING

import click

from grotten import __version__
from grotten.actions import next_actions
from grotten.models import Game

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Message


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    game = Game.create()
    game.describe_location()

    try:
        while game.running and game.lives > 0:
            click.clear()
            show_messages(game.pop_messages())
            action = select_action(next_actions(game))
            game.apply(action)
    except click.exceptions.Abort:
        click.echo()
        click.secho(_("Aborting"), bold=True, fg="yellow")

    click.clear()
    show_messages(game.pop_messages())


def show_messages(messages: List[Message]) -> None:
    for message in messages:
        click.secho(f"[{message.kind}] ", nl=False, fg="magenta")
        click.secho(message.title, bold=True)
        if message.content is not None:
            click.secho(message.content)
        click.echo()


def select_action(actions: List[Action]) -> Action:
    click.secho(_("What do you want to do?"), fg="blue")

    for i, action in enumerate(actions, 1):
        click.secho(f"[{i}] ", nl=False, fg="yellow")
        click.secho(str(action))

    num = click.prompt(
        click.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(actions)),
    )
    click.echo()

    action = actions[num - 1]
    return action
