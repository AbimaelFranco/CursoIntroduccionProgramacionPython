"""
Archivo principal del Dino Game.
"""

import pygame
import random
import sys

from config import SCREEN, CLOCK, FPS, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y
from dinosaur import Dinosaur
from obstacle import Obstacle
from utils import load_best_score, save_best_score, draw_ground, draw_text


def main():
    running = True
    dino = Dinosaur()
    obstacles = []
    spawn_timer = 0
    spawn_interval = 90
    speed = 6
    score = 0
    best_score = load_best_score()
    ground_offset = 0
    game_over = False
    game_over_cooldown = 0
    ducking = False

    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > best_score:
                    save_best_score(score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        dino.jump()
                    if event.key == pygame.K_DOWN:
                        ducking = True
                else:
                    if event.key == pygame.K_r:
                        return main()  # reinicia el juego

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    ducking = False

        if not game_over:
            dino.duck(ducking)
            dino.update()

            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                kind = "cactus" if random.random() < 0.78 else "bird"
                obstacles.append(Obstacle(SCREEN_WIDTH + 10, kind=kind, speed=speed))
                spawn_interval = max(50, int(spawn_interval * 0.985))

            for ob in obstacles[:]:
                ob.speed = speed
                ob.update()
                if ob.is_off_screen():
                    obstacles.remove(ob)

            dino_rect = dino.get_rect()
            for ob in obstacles:
                if dino_rect.colliderect(ob.get_rect()):
                    game_over = True
                    game_over_cooldown = FPS * 0.3
                    if score > best_score:
                        best_score = score
                        save_best_score(best_score)
                    break

            score += 1
            if score % 500 == 0:
                speed += 0.5

            ground_offset = (ground_offset - int(speed)) % 40

        else:
            if game_over_cooldown > 0:
                game_over_cooldown -= 1

        # Dibujar
        SCREEN.fill((235, 235, 235))
        dino.draw(SCREEN)
        for ob in obstacles:
            ob.draw(SCREEN)
        draw_ground(SCREEN, ground_offset)

        draw_text(SCREEN, f"Puntaje: {score}", SCREEN_WIDTH - 160, 10)
        draw_text(SCREEN, f"Mejor: {best_score}", SCREEN_WIDTH - 160, 35)

        if game_over:
            draw_text(SCREEN, "GAME OVER", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, size=28, color=(180, 0, 0))
            draw_text(SCREEN, "Presiona R para reiniciar", SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 10, size=18)

        pygame.display.flip()


if __name__ == "__main__":
    main()
