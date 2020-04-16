import pytest

from grotten.models import Game


@pytest.fixture
def game():
    return Game.create()
