from __future__ import annotations

import copy
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grotten.models import Level


def load_level(level_number: int) -> Level:
    mod = import_module(f".level_{level_number}", __package__)
    level: Level = mod.level  # type: ignore
    return copy.deepcopy(level)
