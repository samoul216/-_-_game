import pygame
import os

def load_enemy_animations(enemy_name):
    animation_types = ['walk', 'attack', 'death']
    animation_list = []

    for animation in animation_types:
        temp_list = []
        folder_path = f'img/enemies/{enemy_name}/{animation}'
        for file_name in sorted(os.listdir(folder_path), key=lambda x: int(x.split('.')[0])):
            img_path = os.path.join(folder_path, file_name)
            image = pygame.image.load(img_path).convert_alpha()
            temp_list.append(image)
        animation_list.append(temp_list)

    return animation_list
