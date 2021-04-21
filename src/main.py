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

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
