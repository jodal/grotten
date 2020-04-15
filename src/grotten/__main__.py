import gettext
from gettext import gettext as _
from pathlib import Path

import click

from grotten import ui
from grotten.models import Game


def main() -> None:
    gettext.bindtextdomain("messages", str(Path(__file__).parent / "locale"))
    gettext.textdomain("messages")

    ui.clear()
    ui.banner(_("Welcome to Grotten!"))

    game = Game.create()

    try:
        while not game.game_done and game.lives > 0:
            game.tick()
    except click.exceptions.Abort:
        ui.banner(_("Aborting"))

    if game.game_done is True:
        ui.banner(_("Welcome back"))
    if game.lives == 0:
        ui.banner(_("Game over"))


if __name__ == "__main__":
    main()
