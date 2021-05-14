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

from __future__ import annotations
from annotations import overrides
import math
import pygame
import random
from abc import ABC, abstractmethod

# import enum
# class CollisionBound(enum.Enum):
#     LEFT = 1
#     RIGHT = 2
#     TOP = 3
#     BOTTOM = 4

# Initialize PyGame
pygame.init()

# Background
background = pygame.image.load("background.png")

# Create the Screen
screen = pygame.display.set_mode(size=(800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Constants
PLAYER_SPEED: float = 1.5
PLAYER_MAX_BULLETS: int = 2
BULLET_SPEED: float = 2.0


def main():
    world: World = World(width=800, height=600)
    world.initialize()

    # Game Loop
    running = True
    while running:
        # RGB - Red, Green, Blue
        screen.fill(color=(0, 0, 0))
        # Background Image.
        screen.blit(source=background, dest=(0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If keystroke is pressed, check whether Right or Left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    world.get_player().set_speed(speed=-PLAYER_SPEED)
                if event.key == pygame.K_RIGHT:
                    world.get_player().set_speed(speed=PLAYER_SPEED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    world.get_player().set_speed(0.0)
                elif event.key == pygame.K_SPACE:
                    world.create_bullet()

        world.update_actor_positions()
        world.perform_collision_detection()
        world.draw_actors()
        world.show_score()

        pygame.display.update()


class ImageCache:
    player_image = None
    enemy_image_1 = None
    enemy_image_2 = None
    enemy_image_3 = None
    bullet_image = None

    def init_images(self):
        self.player_image = pygame.image.load("player.png")
        self.enemy_image_1 = pygame.image.load("enemy_1.png")
        self.enemy_image_2 = pygame.image.load("enemy_2.png")
        self.enemy_image_3 = pygame.image.load("enemy_3.png")
        self.bullet_image = pygame.image.load("bullet.png")


class World:
    """
    The Game World. May be expanded to contain all the things (Players, Enemies, etc).
    """
    width: float = 0.0
    height: float = 0.0

    players: list = list()
    enemies: list = list()
    bullets: list = list()

    image_cache = ImageCache()

    font: pygame.font.Font = pygame.font.Font('freesansbold.ttf', 36)
    score_x_pos: int = 10
    score_y_pos: int = 10
    score: int = 0

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def show_score(self):
        # Functions that are implemented in C do not have names for their arguments,
        # and you need to provide positional-only arguments.
        score_text: pygame.Surface = self.font.render(
            "Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(source=score_text, dest=(self.score_x_pos, self.score_y_pos))

    def initialize(self):
        self.image_cache.init_images()

        player: Player = Player(self.image_cache.player_image)
        player.set_position(x=370.0, y=480.0)
        self.players.append(player)

        x = random.randint(0, self.width - 64)
        y = random.randint(50, 150)

        print(str.format("world.x={}, world.y={}", x, y))

        self.add_enemy(Enemy(image=self.image_cache.enemy_image_1), x, y)
        self.add_enemy(Enemy(image=self.image_cache.enemy_image_1), x, y)
        self.add_enemy(Enemy(image=self.image_cache.enemy_image_1), x, y)

        y += 60
        self.add_enemy(Enemy(image=self.image_cache.enemy_image_2), x, y)
        self.add_enemy(Enemy(image=self.image_cache.enemy_image_2), x, y)
        self.add_enemy(Enemy(image=self.image_cache.enemy_image_2), x, y)

    def get_player(self) -> Player:
        return self.players[0]

    def add_enemy(self, enemy: Enemy, x: int, y: int):
        width: float = enemy.width

        if len(self.enemies) > 0:
            last_enemy: Enemy = self.enemies[-1]
            x = last_enemy.x_pos + (width * 1.5)

        enemy.set_position(x, y)
        self.enemies.append(enemy)

    def update_actor_positions(self):
        self.__update_positions(self.players)
        self.__update_positions(self.enemies)
        self.__update_positions(self.bullets)

        bullets_to_remove = list()
        for bullet in self.bullets:
            if bullet.should_destroy(world=self):
                bullets_to_remove.append(bullet)

        self.__destroy_bullets(bullets_to_remove)

    def __destroy_bullet(self, bullet: Bullet):
        self.bullets.remove(bullet)

    def __destroy_bullets(self, bullets_to_remove: list):
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

    def draw_actors(self):
        for player in self.players:
            player.draw()

        for enemy in self.enemies:
            enemy.draw()

        for bullet in self.bullets:
            bullet.draw()

    def perform_collision_detection(self):
        for enemy in self.enemies:
            for bullet in self.bullets:
                if bullet.is_collision(enemy):
                    print("Collision! Need to destroy enemy: " + str(enemy))
                    self.__destroy_bullet(bullet)
                    enemy.destroy_and_respawn()
                    self.score += 1
                    print(str.format("Score={}", self.score))

    def create_bullet(self):
        """
        Creates a bullet instance at the Player's current position.
        Enforces a maximum number of Player projectiles.
        """
        if len(self.bullets) >= PLAYER_MAX_BULLETS:
            print("Maximum number of bullets reached.")
            return

        bullet: Bullet = Bullet(image=self.image_cache.bullet_image)
        bullet.create(self.get_player(), BULLET_SPEED)
        self.bullets.append(bullet)

    def __update_positions(self, actors: list):
        for actor in actors:
            actor.update_position()
            actor.handle_world_collision(world=self)


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
    def on_world_boundary_collision(self, world: World):
        pass

    def get_x_center(self) -> float:
        return (self.x_pos + self.width) / 2.0

    def get_y_center(self) -> float:
        return (self.y_pos - self.height) / 2.0

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

    def draw(self):
        screen.blit(source=self.image, dest=(self.x_pos, self.y_pos))


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
    def on_world_boundary_collision(self, world: World):
        if self.x_pos <= 0.0:
            self.x_pos = 0.0
        elif self.x_pos >= (world.width - self.width):
            self.x_pos = world.width - self.width

        if self.y_pos >= world.height:
            # Reset position to top of screen.
            self.y_pos = world.height - self.height


# TODO: Optimize this by adding a 'Projectile Pool' from which Bullet instances
# can be acquired and recycled.
class Bullet(Actor):
    """
    The Bullets fired from the Player's spaceship.
    """

    vertical_speed: float = 0.0

    def create(self, player: Player, speed: float):
        self.x_pos = player.x_pos
        self.y_pos = player.y_pos
        self.vertical_speed = speed
        print(str.format("Bullet Created : x={}, y={}, speed={}",
                         self.x_pos, self.y_pos, self.vertical_speed))

    @overrides(Actor)
    def update_position(self):
        self.y_pos -= self.vertical_speed

    @overrides(Actor)
    def on_world_boundary_collision(self, world: World):
        pass

    def should_destroy(self, world: World) -> bool:
        return (self.x_pos < 0 or self.x_pos > world.width
                or self.y_pos < 0 or self.y_pos > world.height)

    def is_collision(self, enemy: Enemy) -> bool:
        distance: float = math.sqrt(
            math.pow(enemy.get_x_center() - self.get_x_center(), 2) +
            math.pow(enemy.get_y_center() - self.get_y_center(), 2))
        # if distance < 50:
        #     print(str.format("Close bullet collision : distance={}", distance))

        return distance < 24


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


if __name__ == '__main__':
    main()
