import pygame

def handle_events(game_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

import pygame
import random
from enemy import Enemy
from assets import load_enemy_animations  # تأكد أن هذه الدالة موجودة لتحميل صور العدو

ENEMY_SPAWN_DELAY = 2000  # ميلي ثانية
last_enemy_spawn_time = pygame.time.get_ticks()

def spawn_enemies(game_state):
    global last_enemy_spawn_time
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
        animation_list = load_enemy_animations("goblin")  # نوع العدو (اسم مجلد الصور)
        x = 900  # جهة اليمين خارج الشاشة
        y = 360
        speed = 2 + game_state.level * 0.2
        new_enemy = Enemy(health=5, animation_list=animation_list, x=x, y=y, speed=speed)
        game_state.enemies.append(new_enemy)
        last_enemy_spawn_time = current_time

def update_enemies(game_state):
    for enemy in game_state.enemies:
        enemy.update()
    for enemy in game_state.enemies:
        enemy.update(target_x=200)  # موقع القلعة
