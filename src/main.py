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
    player: Player = Player(image=playerImg, width=64, height=64)
    enemy: Enemy = Enemy(image=enemyImg, width=64, height=64)

    player.set_position(x=370.0, y=480.0)
    enemy.set_position(x=370.0, y=50.0)

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
                    player.set_speed(speed=-PLAYER_SPEED)
                if event.key == pygame.K_RIGHT:
                    print("Right arrow is pressed")
                    player.set_speed(speed=PLAYER_SPEED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    print("Keystroke has been released")
                    player.set_speed(0.0)

        # 5 = 5 + 0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1

        # Update player position.
        player.update_position(world=world)
        player.draw()

        # Update enemy position.
        enemy.update_position(world=world)
        enemy.draw()

        pygame.display.update()


class World:
    """
    The Game World. May be expanded to contain all the things (Players, Enemies, etc).
    """
    width: float = 0.0
    height: float = 0.0

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height


class Player:
    """
    The Player, controller by input from the user.
    """
    image: pygame.Surface = None

    width: float = 0.0
    height: float = 0.0

    x_pos: float = 0.0
    y_pos: float = 0.0

    horizontal_speed: float = 0.0

    def __init__(self, image: pygame.Surface, width: float, height: float):
        self.image = image
        self.width = width
        self.height = height

    def set_position(self, x: float, y: float):
        self.x_pos = x
        self.y_pos = y

    def set_speed(self, speed: float):
        self.horizontal_speed = speed

    def update_position(self, world: World):
        self.x_pos += self.horizontal_speed
        self.handle_world_collision(world=world)

    def handle_world_collision(self, world: World):
        if self.x_pos <= 0:
            self.x_pos = 0
        elif self.x_pos >= (world.width - self.width):
            self.x_pos = world.width - self.width

    def draw(self):
        screen.blit(source=self.image, dest=(self.x_pos, self.y_pos))


class Enemy(Player):
    pass


if __name__ == '__main__':
    main()
