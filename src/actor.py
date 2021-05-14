from __future__ import annotations

import pygame

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Workaround for Circular Type Hinting Circular Dependencies
if TYPE_CHECKING:
    from world import World


# TODO: Investigate a way to remove the circular dependency on World.
class Actor(ABC):
    """
    An Abstract-Base-Class that defines an actor in our world. Ex: A player or an enemy.
    """

    image: pygame.Surface = None

    width: float = 0.0
    height: float = 0.0

    x_pos: float = 0.0
    y_pos: float = 0.0

    def __init__(self, image: pygame.Surface):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

        print(str.format("width={}, height={}", self.width, self.height))

    @abstractmethod
    def update_position(self):
        pass

    @abstractmethod
    def on_world_boundary_collision(self, world: 'World'):
        pass

    def get_x_center(self) -> float:
        return (self.x_pos + self.width) / 2.0

    def get_y_center(self) -> float:
        return (self.y_pos - self.height) / 2.0

    def set_position(self, x: float, y: float):
        self.x_pos = x
        self.y_pos = y

    def handle_world_collision(self, world: 'World'):
        # Handle horizontal collisions (left and right sides)
        if self.x_pos <= 0.0:
            # Left side collision.
            self.on_world_boundary_collision(world=world)
        elif self.x_pos >= (world.width - self.width):
            # Right side collision.
            self.on_world_boundary_collision(world=world)

        # Handle vertical collisions (top and bottom)
        if self.y_pos > world.height:
            # Bottom edge collision.
            self.on_world_boundary_collision(world=world)
        elif self.y_pos < 0.0:
            # Top edge collision.
            self.on_world_boundary_collision(world=world)

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.image, dest=(self.x_pos, self.y_pos))
