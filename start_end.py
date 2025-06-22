
import pygame

def draw_start_screen(screen):
    font = pygame.font.SysFont("arial", 48)
    title_text = font.render("Castle Defender", True, (255, 255, 255))
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))

    button_font = pygame.font.SysFont("arial", 36)
    start_text = button_font.render("Click to Start", True, (255, 255, 255))
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 300))

def draw_game_over_screen(screen, score):
    font = pygame.font.SysFont("arial", 48)
    over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(over_text, (screen.get_width() // 2 - over_text.get_width() // 2, 200))

    score_text = pygame.font.SysFont("arial", 36).render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 270))

    restart_text = pygame.font.SysFont("arial", 28).render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 330))
