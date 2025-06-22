
import pygame

def draw_game(screen, game_state):
    # Load background
    bg_img = pygame.image.load("img/bg.png").convert()
    screen.blit(bg_img, (0, 0))

    # Draw enemies
    for enemy in game_state.enemies:
        enemy.draw(screen)

    # Draw castle (optional, static image at bottom-right)
    castle_img = pygame.image.load("img/castle/castle_100.png").convert_alpha()
    screen.blit(castle_img, (600, 350))

    # Draw health text (optional)
    font = pygame.font.SysFont("arial", 20)
    health_text = font.render(f"Health: {game_state.castle_health}/100", True, (0, 0, 0))
    screen.blit(health_text, (850, 570))
