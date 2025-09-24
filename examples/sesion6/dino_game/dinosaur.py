"""
Clase Dinosaur: jugador principal.
"""

import pygame
from config import GROUND_Y, WHITE


class Dinosaur:
    """
    Representa al dinosaurio del jugador, con lógica de correr y saltar.
    """

    def __init__(self, x=50, y=GROUND_Y - 40):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 40
        self.color = (83, 83, 83)
        self.vel_y = 0
        self.jump_strength = -12
        self.gravity = 0.6
        self.on_ground = True
        self.run_anim_index = 0
        self.run_anim_timer = 0

    def jump(self):
        """Inicia salto si está en el suelo."""
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def duck(self, ducking):
        """Agacha al dino si está en el suelo."""
        if ducking and self.on_ground:
            self.height = 24
        else:
            self.height = 40

    def update(self):
        """Actualiza física y animación."""
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

        self.run_anim_timer += 1
        if self.run_anim_timer > 6:
            self.run_anim_timer = 0
            self.run_anim_index = (self.run_anim_index + 1) % 2

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        """Dibuja el dino en pantalla."""
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect)
        eye = (rect.x + 30, rect.y + 8, 6, 6)
        pygame.draw.ellipse(surface, WHITE, eye)
        if self.on_ground:
            if self.run_anim_index == 0:
                leg1 = (rect.x + 10, rect.y + self.height, 8, 8)
                leg2 = (rect.x + 26, rect.y + self.height, 8, 8)
            else:
                leg1 = (rect.x + 10, rect.y + self.height, 8, 8)
                leg2 = (rect.x + 22, rect.y + self.height, 8, 8)
            pygame.draw.rect(surface, self.color, leg1)
            pygame.draw.rect(surface, self.color, leg2)
        else:
            leg = (rect.x + 18, rect.y + self.height - 2, 8, 6)
            pygame.draw.rect(surface, self.color, leg)
