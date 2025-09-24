"""
Funciones auxiliares para el juego.
"""

import pygame
import os
from config import DARK_GRAY, SCREEN_WIDTH, GROUND_Y, FONT, BEST_SCORE_FILE


def load_best_score():
    if os.path.exists(BEST_SCORE_FILE):
        try:
            with open(BEST_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except Exception:
            return 0
    return 0


def save_best_score(score):
    try:
        with open(BEST_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass


def draw_ground(surface, offset):
    pygame.draw.line(surface, DARK_GRAY, (0, GROUND_Y + 1), (SCREEN_WIDTH, GROUND_Y + 1), 3)
    spacing = 40
    for i in range(-1, SCREEN_WIDTH // spacing + 2):
        x = (i * spacing + offset) % (spacing * 4)
        pygame.draw.rect(surface, DARK_GRAY, (x, GROUND_Y + 4, 10, 6))


def draw_text(surface, text, x, y, size=20, color=(0, 0, 0)):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))
