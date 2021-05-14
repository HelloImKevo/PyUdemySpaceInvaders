from __future__ import annotations

import random
import pygame

from imagecache import ImageCache
from player import Player
from enemy import Enemy
from bullet import Bullet

PLAYER_MAX_BULLETS: int = 2
BULLET_SPEED: float = 2.0


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

    font: pygame.font.Font = None
    score_x_pos: int = 10
    score_y_pos: int = 10
    score: int = 0

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.font = pygame.font.Font('freesansbold.ttf', 36)

    def show_score(self):
        from main import screen
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

    def get_player(self) -> 'Player':
        return self.players[0]

    def add_enemy(self, enemy: 'Enemy', x: int, y: int):
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

    def __destroy_bullet(self, bullet: 'Bullet'):
        self.bullets.remove(bullet)

    def __destroy_bullets(self, bullets_to_remove: list):
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

    def draw_actors(self):
        from main import screen
        for player in self.players:
            player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

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
