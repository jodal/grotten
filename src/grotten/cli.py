from __future__ import annotations

from gettext import gettext as _
from typing import List, Optional, TYPE_CHECKING

import click
from click import secho as p

from grotten.actions import next_actions
from grotten.models import Game

if TYPE_CHECKING:
    from grotten.actions import Action
    from grotten.models import Item, Location, Message


def main() -> None:
    click.clear()
    banner(_("Welcome to Grotten!"))

    game = Game.create()

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
    describe_location(game.location)
    show_messages(game.tick.messages)

    game.begin_tick()

    if game.location.effect is not None:
        game.location.effect(game)

    if game.tick.actions_allowed:
        action = select_action(next_actions(game))
        action.apply(game)

    if game.tick.inventory_open:
        show_inventory(game.inventory)

    click.clear()


def describe_location(location: Location) -> None:
    describe(
        kind=_("location"),
        value=location.name,
        description=location.description,
    )
    for item in location.items:
        describe(kind=_("item"), value=item.name)


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
