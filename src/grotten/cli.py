from __future__ import annotations

from gettext import gettext as _
from typing import TYPE_CHECKING

import click
import rich
import typer

from grotten.actions import Action
from grotten.game import Game
from grotten.levels import get_levels, load_level

if TYPE_CHECKING:
    from grotten.models import Message


app = typer.Typer()


@app.command()
def play() -> None:
    start_game()


@app.command()
def levels() -> None:
    levels = get_levels()

    for level in get_levels():
        rich.print(rf"[yellow]\[{level.number}] ", end="")
        rich.print(level.name)

    level_number: int = typer.prompt(
        typer.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(levels)),
    )
    typer.echo()

    start_game(level_number=level_number)


def start_game(*, level_number: int = 1) -> None:
    game = Game.create(level=load_level(level_number))
    game.describe_location()

    try:
        while game.running and game.lives > 0:
            typer.clear()
            show_messages(game.messages.pop())
            action = select_action(game.available_actions())
            action.apply(game)
    except typer.Abort:
        rich.print()
        rich.print(f"[bold yellow]{_('Aborting')}")

    typer.clear()
    show_messages(game.messages.pop())


def show_messages(messages: list[Message]) -> None:
    for message in messages:
        rich.print(rf"[magenta]\[{_(message.kind.value)}] ", end="")
        rich.print(f"[bold]{message.title}")
        if message.content is not None:
            rich.print(message.content)
        rich.print()


def select_action(actions: list[Action]) -> Action:
    typer.secho(_("What do you want to do?"), fg="blue")

    for i, action in enumerate(actions, 1):
        rich.print(rf"[yellow]\[{i}] ", end="")
        if action.is_meta_action():
            rich.print(f"[white]{action}")
        else:
            rich.print(str(action))

    num: int = typer.prompt(
        typer.style(_("Select"), fg="blue"),
        type=click.IntRange(min=1, max=len(actions)),
    )
    rich.print()

    return actions[num - 1]
