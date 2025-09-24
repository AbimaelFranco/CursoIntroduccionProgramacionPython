"""
Clase Obstacle: cactus y pájaros.
"""

import pygame
import random
from config import GROUND_Y, BLACK


class Obstacle:
    """
    Obstáculo: cactus o pájaro.
    """

    def __init__(self, x, kind="cactus", speed=6):
        self.x = x
        self.kind = kind
        self.speed = speed

        if kind == "cactus":
            self.width = random.choice([20, 24, 28])
            self.height = random.choice([34, 38])
            self.y = GROUND_Y - self.height
            self.color = (40, 160, 40)
        else:
            self.width = 34
            self.height = 24
            self.y = random.choice([GROUND_Y - 80, GROUND_Y - 120])
            self.color = (30, 30, 120)

        self.anim_index = 0
        self.anim_timer = 0

    def update(self):
        self.x -= self.speed
        if self.kind == "bird":
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 2

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect)
        if self.kind == "bird":
            if self.anim_index == 0:
                wing1 = (rect.x + 4, rect.y + 2, 8, 4)
                wing2 = (rect.x + 22, rect.y + 2, 8, 4)
            else:
                wing1 = (rect.x + 6, rect.y, 8, 4)
                wing2 = (rect.x + 20, rect.y + 4, 8, 4)
            pygame.draw.rect(surface, BLACK, wing1)
            pygame.draw.rect(surface, BLACK, wing2)
