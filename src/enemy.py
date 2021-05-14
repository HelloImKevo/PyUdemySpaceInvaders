from __future__ import annotations

import random

from actor import Actor
from annotations import overrides
from typing import TYPE_CHECKING

# Workaround for Circular Type Hinting Circular Dependencies
if TYPE_CHECKING:
    from world import World


# TODO: We need an Enemy container to keep all the Y-axis positions in-sync
# (all the enemies should move in unison)
class Enemy(Actor):
    """
    An Enemy, controlled by game logic.
    """

    STARTING_SPEED: int = 1

    # Initialize starting speed.
    horizontal_speed: float = STARTING_SPEED

    def increase_speed(self, amount: float):
        if self.horizontal_speed > 0.0:
            self.horizontal_speed += amount
        else:
            self.horizontal_speed -= amount

    @overrides(Actor)
    def update_position(self):
        self.x_pos += self.horizontal_speed

    @overrides(Actor)
    def on_world_boundary_collision(self, world: World):
        print(str.format("x={}, y={}", self.x_pos, self.y_pos))

        # Reverse horizontal speed.
        self.horizontal_speed *= -1.0
        # Move enemy down.
        self.y_pos += 24.00
        # Increase enemy speed.
        self.increase_speed(0.1)

        # Handle left side collision correction.
        if self.x_pos <= 0.0:
            self.x_pos = 0.0
        # Handle right side collision correction.
        elif self.x_pos >= (world.width - self.width):
            self.x_pos = world.width - self.width

        if self.y_pos >= world.height:
            # Reset position to top of screen.
            self.y_pos = self.height
            self.horizontal_speed = 2.0

    def destroy_and_respawn(self):
        x = random.randint(0, self.width - 64)
        y = random.randint(50, 150)
        self.x_pos = x
        self.y_pos = y
        self.horizontal_speed = self.STARTING_SPEED
