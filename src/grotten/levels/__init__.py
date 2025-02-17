from __future__ import annotations

import copy
import pathlib
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grotten.models import Level


def get_levels() -> list[Level]:
    level_dir = pathlib.Path(__file__).parent
    levels = []
    for level_file in level_dir.glob("level_*.py"):
        level_number = int(level_file.name.replace("level_", "").replace(".py", ""))
        levels.append(load_level(level_number))
    return levels


def load_level(level_number: int) -> Level:
    mod = import_module(f".level_{level_number}", __package__)
    level: Level = mod.level
    return copy.deepcopy(level)
