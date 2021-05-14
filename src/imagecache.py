import pygame


class ImageCache:
    player_image = None
    enemy_image_1 = None
    enemy_image_2 = None
    enemy_image_3 = None
    bullet_image = None

    def init_images(self):
        self.player_image = pygame.image.load("assets/player.png")
        self.enemy_image_1 = pygame.image.load("assets/enemy_1.png")
        self.enemy_image_2 = pygame.image.load("assets/enemy_2.png")
        self.enemy_image_3 = pygame.image.load("assets/enemy_3.png")
        self.bullet_image = pygame.image.load("assets/bullet.png")
