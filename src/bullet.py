from __future__ import annotations

import math

from actor import Actor
from annotations import overrides
from typing import TYPE_CHECKING

# Workaround for Circular Type Hinting Circular Dependencies
if TYPE_CHECKING:
    from world import World
    from enemy import Enemy
    from player import Player


# TODO: Optimize this by adding a 'Projectile Pool' from which Bullet instances
# can be acquired and recycled.
class Bullet(Actor):
    """
    The Bullets fired from the Player's spaceship.
    """

    vertical_speed: float = 0.0

    def create(self, player: 'Player', speed: float):
        self.x_pos = player.x_pos
        self.y_pos = player.y_pos
        self.vertical_speed = speed
        print(str.format("Bullet Created : x={}, y={}, speed={}",
                         self.x_pos, self.y_pos, self.vertical_speed))

    @overrides(Actor)
    def update_position(self):
        self.y_pos -= self.vertical_speed

    @overrides(Actor)
    def on_world_boundary_collision(self, world: 'World'):
        pass

    def should_destroy(self, world: 'World') -> bool:
        return (self.x_pos < 0 or self.x_pos > world.width
                or self.y_pos < 0 or self.y_pos > world.height)

    def is_collision(self, enemy: 'Enemy') -> bool:
        distance: float = math.sqrt(
            math.pow(enemy.get_x_center() - self.get_x_center(), 2) +
            math.pow(enemy.get_y_center() - self.get_y_center(), 2))
        # if distance < 50:
        #     print(str.format("Close bullet collision : distance={}", distance))

        return distance < 24
