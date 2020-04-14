import pytest

from grotten import actions
from grotten.actions import next_actions
from grotten.levels import level_1
from grotten.models import Direction, Game


@pytest.fixture
def game() -> Game:
    return Game.create()


def test_exit_str():
    action = actions.Exit()

    assert str(action) == "Exit game"


def test_exit_apply(game: Game):
    action = actions.Exit()
    assert game.game_done is False

    action.apply(game)

    assert game.game_done is True


def test_go_str():
    action = actions.Go(direction=Direction.NORTH)

    assert str(action) == "Go North"


def test_go_apply(game: Game):
    action = actions.Go(direction=Direction.WEST)
    assert game.location == level_1.entrance

    action.apply(game)

    assert game.location == level_1.skeletons


def test_next_actions(game: Game):
    result = next_actions(game)

    assert result == [
        actions.Go(direction=Direction.NORTH),
        actions.Go(direction=Direction.WEST),
        actions.Exit(),
    ]
