from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction
from gettext import gettext as _
from gettext import ngettext

from grotten import actions
from grotten.enums import Direction, Kind
from grotten.levels import load_level
from grotten.models import (
    Creature,
    Inventory,
    Item,
    Level,
    Location,
    Mailbox,
)


@dataclass
class Game:
    level: Level
    location: Location
    inventory: Inventory = field(default_factory=Inventory)
    lives: int = 3
    running: bool = True
    messages: Mailbox = field(default_factory=Mailbox)

    @classmethod
    def create(cls, *, level: Level | None = None) -> Game:
        if level is None:
            level = load_level(1)
        return cls(level=level, location=level.start)

    # --- Actions

    def available_actions(self) -> list[actions.Action]:
        return [
            *self.location.actions,
            *[
                actions.Attack(creature=creature)
                for creature in self.location.creatures
            ],
            *[actions.PickUp(item=item) for item in self.location.items],
            *[
                actions.Go(direction=direction)
                for direction in Direction
                if direction in self.location.neighbors
            ],
            actions.ShowInventory(),
            actions.EndGame(),
        ]

    def end_game(self) -> None:
        self.running = False
        self.messages.add(kind=Kind.GAME, title=_("Welcome back"))

    def go(self, direction: Direction) -> None:
        self.location = self.location.neighbors[direction]
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Going {direction}").format(direction=_(direction.value)),
        )
        self.describe_location()
        if self.location.effect is not None:
            self.location.effect(self)

    def attack(self, creature: Creature) -> Fraction:
        weapon = self.inventory.get_weapon()
        winning_odds = Fraction(weapon.attack_strength, creature.strength)
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Attack {creature}").format(creature=creature.name),
            content=_(
                "You attack {creature} ({creature_strength}) "
                "with {weapon} ({weapon_strength})."
            ).format(
                creature=creature.name,
                creature_strength=creature.strength,
                weapon=weapon.name,
                weapon_strength=weapon.attack_strength,
            ),
        )

        won = random.random() < winning_odds  # noqa: S311

        if won:
            self.win_fight(creature)
        else:
            self.lose_fight(creature)

        return winning_odds

    def pick_up(self, item: Item) -> None:
        self.location.items.remove(item)
        self.inventory.add(item)
        self.messages.add(
            kind=Kind.ACTION,
            title=_("Picking up {item}").format(item=item.name),
        )

    def show_inventory(self) -> None:
        if not self.inventory.items:
            self.messages.add(
                kind=Kind.INVENTORY,
                title=_("empty"),
                content=_("The inventory is empty."),
            )

        for item in self.inventory.items:
            self.messages.add(kind=Kind.INVENTORY, title=item.name)

    # --- Action building blocks

    def describe_location(self) -> None:
        self.messages.add(
            kind=Kind.LOCATION,
            title=self.location.name,
            content=self.location.description,
        )

        for creature in self.location.creatures:
            self.messages.add(kind=Kind.CREATURE, title=creature.name)

        for item in self.location.items:
            self.messages.add(kind=Kind.ITEM, title=item.name)

    def win_fight(self, creature: Creature) -> None:
        self.messages.add(
            kind=Kind.ACTION,
            title=_("You won"),
            content=_("You defeated {creature}.").format(creature=creature.name),
        )
        self.location.creatures.remove(creature)
        self.location.items.extend(creature.loot)

    def lose_fight(self, creature: Creature) -> None:
        self.messages.add(
            kind=Kind.ACTION,
            title=_("You lost"),
            content=_("You lost the battle with {creature}.").format(
                creature=creature.name
            ),
        )
        self.die()

    def die(self) -> None:
        self.lives -= 1
        self.messages.add(
            kind=Kind.LIFE,
            title=_("You died"),
            content=ngettext(
                _("You have only {lives} life left."),
                _("You have {lives} lives left."),
                self.lives,
            ).format(lives=self.lives),
        )
        if self.lives == 0:
            self.messages.add(kind=Kind.GAME, title=_("Game over"))

    def restart_level(self) -> None:
        self.location = self.level.start
        self.messages.add(
            kind=Kind.LEVEL,
            title=_("Restart"),
            content=_("You respawn at the beginning."),
        )
