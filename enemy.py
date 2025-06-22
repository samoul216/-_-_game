import pygame
import math
import random

class EnemyState:
    IDLE = "idle"
    WALK = "walk"
    ATTACK = "attack"
    DEAD = "dead"

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        super().__init__()
        self.state = EnemyState.WALK
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.alive = True

    def update(self, screen=None, castle=None, bullet_group=None, target_x=200):
        if self.health <= 0:
            self.state = EnemyState.DEAD
        elif abs(self.rect.centerx - target_x) < 40:
            self.state = EnemyState.ATTACK
        else:
            self.state = EnemyState.WALK

        if self.state == EnemyState.DEAD:
            self.action = 2
        elif self.state == EnemyState.ATTACK:
            self.action = 1
        else:
            self.action = 0
            if self.rect.centerx > target_x:
                self.rect.x -= self.speed

        # Update animation
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.state == EnemyState.DEAD:
                    self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def hit(self):
        self.health -= 1
