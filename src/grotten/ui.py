from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import click

from grotten.i18n import _

if TYPE_CHECKING:
    from grotten.actions import Action


p = click.secho


def clear() -> None:
    click.clear()


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