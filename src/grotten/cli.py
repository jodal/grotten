from __future__ import annotations

from gettext import gettext as _
from typing import TYPE_CHECKING

import click

from grotten import __version__
from grotten.game import Game
from grotten.levels import get_levels, load_level

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Message


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command()
def play() -> None:
    start_game()


@cli.command()
def levels() -> None:
    levels = get_levels()

    for level in get_levels():
        click.secho(f"[{level.number}] ", nl=False, fg="yellow")
        click.echo(level.name)

    level_number = click.prompt(
        click.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(levels)),
    )
    click.echo()

    start_game(level_number=level_number)


def start_game(*, level_number: int = 1) -> None:
    game = Game.create(level=load_level(level_number))
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


def show_messages(messages: list[Message]) -> None:
    for message in messages:
        click.secho(f"[{_(message.kind)}] ", nl=False, fg="magenta")
        click.secho(message.title, bold=True)
        if message.content is not None:
            click.secho(message.content)
        click.echo()


def select_action(actions: list[Action]) -> Action:
    click.secho(_("What do you want to do?"), fg="blue")

    for i, action in enumerate(actions, 1):
        click.secho(f"[{i}] ", nl=False, fg="yellow")
        click.secho(str(action), fg="white" if action.is_meta_action() else None)

    num = click.prompt(
        click.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(actions)),
    )
    click.echo()

    return actions[num - 1]
