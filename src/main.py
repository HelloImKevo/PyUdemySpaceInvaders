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
playerX = 370
playerY = 480


def main():
    # Game Loop
    running = True
    while running:
        # RGB - Red, Green, Blue
        screen.fill(color=(0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player()
        pygame.display.update()


def player():
    screen.blit(source=playerImg, dest=(playerX, playerY))


if __name__ == '__main__':
    main()
