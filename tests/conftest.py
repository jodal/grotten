import pytest

from grotten.levels import load_level
from grotten.models import Game


@pytest.fixture
def level_1():
    return load_level(1)


@pytest.fixture
def game(level_1):
    return Game.create(level=level_1)
