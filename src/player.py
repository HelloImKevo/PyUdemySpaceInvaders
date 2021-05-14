from __future__ import annotations

from actor import Actor
from annotations import overrides
from typing import TYPE_CHECKING

# Workaround for Circular Type Hinting Circular Dependencies
if TYPE_CHECKING:
    from world import World


class Player(Actor):
    """
    The Player, controlled by input from the user.
    """

    horizontal_speed: float = 0.0

    def set_speed(self, speed: float):
        self.horizontal_speed = speed

    @overrides(Actor)
    def update_position(self):
        self.x_pos += self.horizontal_speed

    @overrides(Actor)
    def on_world_boundary_collision(self, world: 'World'):
        if self.x_pos <= 0.0:
            self.x_pos = 0.0
        elif self.x_pos >= (world.width - self.width):
            self.x_pos = world.width - self.width

        if self.y_pos >= world.height:
            # Reset position to top of screen.
            self.y_pos = world.height - self.height
