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

import pygame
from pygame import mixer

from world import World

# Initialize PyGame
pygame.init()

# Background
background = pygame.image.load("assets/background.png")

# Background Music
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# Create the Screen
screen: pygame.Surface = pygame.display.set_mode(size=(800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/ufo.png")
pygame.display.set_icon(icon)

# Constants
PLAYER_SPEED: float = 1.5


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


if __name__ == '__main__':
    main()
