import pygame
from model import GameState
from view import draw_game
from controller import handle_events, spawn_enemies, update_enemies
from start_end import draw_start_screen, draw_game_over_screen
import os

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Castle Defender")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# Load background music
pygame.mixer.music.load("audio/music2.mp3")
pygame.mixer.music.play(-1)

def game_loop():
    game_state = GameState()
    running = True
    game_over = False
    show_start = True

    while running:
        clock.tick(60)

        if show_start:
            screen.fill((0, 0, 0))
            draw_start_screen(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_start = False
            continue

        if game_over:
            screen.fill((0, 0, 0))
            draw_game_over_screen(screen, game_state.score)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_state = GameState()
                    game_over = False
                    show_start = True
            continue

        screen.fill((0, 0, 0))
        if not handle_events(game_state):
            break
        spawn_enemies(game_state)
        update_enemies(game_state)
        draw_game(screen, game_state)

        if game_state.castle_health <= 0:
            game_over = True

        pygame.display.flip()

    pygame.quit()

game_loop()
