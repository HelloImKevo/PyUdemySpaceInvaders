#!/usr/bin/env python3

"""
|   _____ ______   ___   _____  _____   _____  _   _  _   _   ___  ______  _____ ______  _____
|  /  ___|| ___ \ / _ \ /  __ \|  ___| |_   _|| \ | || | | | / _ \ |  _  \|  ___|| ___ \/  ___|
|  \ `--. | |_/ // /_\ \| /  \/| |__     | |  |  \| || | | |/ /_\ \| | | || |__  | |_/ /\ `--.
|   `--. \|  __/ |  _  || |    |  __|    | |  | . ` || | | ||  _  || | | ||  __| |    /  `--. \
|  /\__/ /| |    | | | || \__/\| |___   _| |_ | |\  |\ \_/ /| | | || |/ / | |___ | |\ \ /\__/ /
|  \____/ \_|    \_| |_/ \____/\____/   \___/ \_| \_/ \___/ \_| |_/|___/  \____/ \_| \_|\____/
|

The arcade classic built with the PyGame engine.

Usage:

    python3 main.py
"""

import pygame
import random
from abc import ABC, abstractmethod
import enum

# Initialize PyGame
pygame.init()

# Create the Screen
screen = pygame.display.set_mode(size=(800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")

# Enemy
enemyImg = pygame.image.load("enemy_1.png")

# Constants
PLAYER_SPEED: float = 1.0


def main():
    world: World = World(width=800, height=600)
    world.init_actors()

    # Game Loop
    running = True
    while running:
        # RGB - Red, Green, Blue
        screen.fill(color=(0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If keystroke is pressed, check whether Right or Left
            if event.type == pygame.KEYDOWN:
                print("A key has been pressed")
                if event.key == pygame.K_LEFT:
                    print("Left arrow is pressed")
                    world.get_player().set_speed(speed=-PLAYER_SPEED)
                if event.key == pygame.K_RIGHT:
                    print("Right arrow is pressed")
                    world.get_player().set_speed(speed=PLAYER_SPEED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    print("Keystroke has been released")
                    world.get_player().set_speed(0.0)

        world.update_actor_positions()
        world.draw_actors()

        pygame.display.update()


class World:
    """
    The Game World. May be expanded to contain all the things (Players, Enemies, etc).
    """
    width: float = 0.0
    height: float = 0.0

    players: list = list()
    enemies: list = list()

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def init_actors(self):
        player: Player = Player(image=pygame.image.load("player.png"))
        player.set_position(x=370.0, y=480.0)
        self.players.append(player)

        x = random.randint(0, self.width - 64)
        y = random.randint(50, 150)

        print(str.format("world.x={}, world.y={}", x, y))

        self.add_enemy(Enemy(image=pygame.image.load("enemy_1.png")), x, y)
        self.add_enemy(Enemy(image=pygame.image.load("enemy_2.png")), x, y)

    def get_player(self):
        return self.players[0]

    def add_enemy(self, enemy, x: int, y: int):
        width: float = enemy.width

        if len(self.enemies) > 0:
            last_enemy: Enemy = self.enemies[-1]
            x = last_enemy.x_pos + (width * 1.5)

        enemy.set_position(x, y)
        self.enemies.append(enemy)

    def update_actor_positions(self):
        for player in self.players:
            player.update_position(world=self)

        for enemy in self.enemies:
            enemy.update_position(world=self)

    def draw_actors(self):
        for player in self.players:
            player.draw()

        for enemy in self.enemies:
            enemy.draw()


# class CollisionBound(enum.Enum):
#     LEFT = 1
#     RIGHT = 2
#     TOP = 3
#     BOTTOM = 4


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

    def set_position(self, x: float, y: float):
        self.x_pos = x
        self.y_pos = y

    def handle_world_collision(self, world: World):
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

    @abstractmethod
    def on_world_boundary_collision(self, world: World):
        pass

    def draw(self):
        screen.blit(source=self.image, dest=(self.x_pos, self.y_pos))


class Player(Actor):
    """
    The Player, controlled by input from the user.
    """

    horizontal_speed: float = 0.0

    def set_speed(self, speed: float):
        self.horizontal_speed = speed

    def update_position(self, world: World):
        self.x_pos += self.horizontal_speed
        self.handle_world_collision(world=world)

    # Override abstract method
    def on_world_boundary_collision(self, world: World):
        if self.x_pos <= 0.0:
            self.x_pos = 0.0
        elif self.x_pos >= (world.width - self.width):
            self.x_pos = world.width - self.width

        if self.y_pos >= world.height:
            # Reset position to top of screen.
            self.y_pos = world.height - self.height


# TODO: We need an Enemy container to keep all the Y-axis positions in-sync
# (all the enemies should move in unison)
class Enemy(Actor):
    """
    An Enemy, controlled by game logic.
    """

    # Initialize starting speed.
    horizontal_speed: float = 1.0

    def increase_speed(self, amount: float):
        if self.horizontal_speed > 0.0:
            self.horizontal_speed += amount
        else:
            self.horizontal_speed -= amount

    def update_position(self, world: World):
        self.x_pos += self.horizontal_speed
        self.handle_world_collision(world=world)

    # Override abstract method
    def on_world_boundary_collision(self, world: World):
        print(str.format("x={}, y={}", self.x_pos, self.y_pos))

        # Reverse horizontal speed.
        self.horizontal_speed *= -1.0
        # Move enemy down.
        self.y_pos += 24.00
        # Increase enemy speed.
        self.increase_speed(0.5)

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


if __name__ == '__main__':
    main()
