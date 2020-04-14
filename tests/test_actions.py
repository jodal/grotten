import pytest

from grotten.actions import ExitAction, GoAction, next_actions
from grotten.levels import level_1
from grotten.models import Direction, Game


@pytest.fixture
def game() -> Game:
    return Game.create()


def test_exit_str():
    action = ExitAction()

    assert str(action) == "Exit game"


def test_exit_apply(game: Game):
    action = ExitAction()
    assert game.game_done is False

    action.apply(game)

    assert game.game_done is True


def test_go_str():
    action = GoAction(direction=Direction.NORTH)

    assert str(action) == "Go North"


def test_go_apply(game: Game):
    action = GoAction(direction=Direction.WEST)
    assert game.location == level_1.entrance

    action.apply(game)

    assert game.location == level_1.dragon_lair


def test_next_actions(game: Game):
    actions = next_actions(game)

    assert actions == [
        GoAction(direction=Direction.NORTH),
        GoAction(direction=Direction.WEST),
        ExitAction(),
    ]
