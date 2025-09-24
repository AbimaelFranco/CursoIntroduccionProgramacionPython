"""
Juego tipo "Dinosaurio de Google" (versión simple) usando Pygame.

Características:
- Dino que corre y salta.
- Obstáculos generados aleatoriamente (cactus y pájaros simples).
- Puntuación que aumenta con el tiempo y aumenta la velocidad.
- Reinicio del juego al chocar.
- Guardado simple del mejor puntaje en 'best_score.txt'.

Autor: (puedes poner tu nombre)
"""

import pygame
import random
import os
import sys

# --- CONFIGURACIÓN GLOBAL ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_Y = 230  # coordenada Y del "suelo"
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)

# Rutas
BEST_SCORE_FILE = "best_score.txt"

# Inicialización de pygame
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino - Juego estilo Chrome")
CLOCK = pygame.time.Clock()

# Fuente
FONT = pygame.font.SysFont("Arial", 20)


def load_best_score():
    """
    Carga el mejor puntaje desde el archivo BEST_SCORE_FILE.

    Returns:
        int: mejor puntaje (0 si no existe).
    """
    if os.path.exists(BEST_SCORE_FILE):
        try:
            with open(BEST_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except Exception:
            return 0
    return 0


def save_best_score(score):
    """
    Guarda el mejor puntaje en BEST_SCORE_FILE.

    Args:
        score (int): puntaje a guardar.
    """
    try:
        with open(BEST_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass


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
        # Para animación simple: alternar entre 2 "frames" de piernas
        self.run_anim_index = 0
        self.run_anim_timer = 0

    def jump(self):
        """Inicia salto si está en el suelo."""
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def duck(self, ducking):
        """
        Ajusta la altura si el jugador está agachado (ducking).
        
        Args:
            ducking (bool): True si se está agachando.
        """
        if ducking and self.on_ground:
            self.height = 24
        else:
            self.height = 40

    def update(self):
        """Actualiza posición y física simple (gravedad)."""
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

        # animación simple
        self.run_anim_timer += 1
        if self.run_anim_timer > 6:
            self.run_anim_timer = 0
            self.run_anim_index = (self.run_anim_index + 1) % 2

    def get_rect(self):
        """Devuelve pygame.Rect de la posición actual (para colisiones)."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        """Dibuja el sprite simple del dinosaurio en la pantalla."""
        rect = self.get_rect()
        # cuerpo
        pygame.draw.rect(surface, self.color, rect)
        # ojo
        eye = (rect.x + 30, rect.y + 8, 6, 6)
        pygame.draw.ellipse(surface, WHITE, eye)
        # piernas (animación simple)
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
            # en el aire: piernas recogidas
            leg = (rect.x + 18, rect.y + self.height - 2, 8, 6)
            pygame.draw.rect(surface, self.color, leg)


class Obstacle:
    """
    Obstáculo base: puede ser cactus (bajo) o pájaro (volando).
    """

    def __init__(self, x, kind="cactus", speed=6):
        self.x = x
        self.kind = kind  # 'cactus' o 'bird'
        self.speed = speed
        if kind == "cactus":
            # varios tamaños para cactus
            self.width = random.choice([20, 24, 28])
            self.height = random.choice([34, 38])
            self.y = GROUND_Y - self.height
            self.color = (40, 160, 40)
        else:  # bird
            self.width = 34
            self.height = 24
            # pájaros pueden estar en dos alturas
            self.y = random.choice([GROUND_Y - 80, GROUND_Y - 120])
            self.color = (30, 30, 120)
        # para animación simple de pájaro
        self.anim_index = 0
        self.anim_timer = 0

    def update(self):
        """Mueve el obstáculo hacia la izquierda."""
        self.x -= self.speed
        # animación simple del pájaro
        if self.kind == "bird":
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 2

    def is_off_screen(self):
        """Devuelve True si el obstáculo ya salió por la izquierda."""
        return self.x + self.width < 0

    def get_rect(self):
        """Devuelve pygame.Rect usado para colisiones."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        """Dibuja el obstáculo (cactus o pájaro)."""
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect)
        if self.kind == "bird":
            # dibuja "alas" sencillas
            if self.anim_index == 0:
                wing1 = (rect.x + 4, rect.y + 2, 8, 4)
                wing2 = (rect.x + 22, rect.y + 2, 8, 4)
            else:
                wing1 = (rect.x + 6, rect.y, 8, 4)
                wing2 = (rect.x + 20, rect.y + 4, 8, 4)
            pygame.draw.rect(surface, BLACK, wing1)
            pygame.draw.rect(surface, BLACK, wing2)


def draw_ground(surface, offset):
    """
    Dibuja la línea de suelo y algunas marcas para dar sensación de movimiento.

    Args:
        offset (int): valor que desplaza las marcas para simular el suelo en movimiento.
    """
    # línea principal del suelo
    pygame.draw.line(surface, DARK_GRAY, (0, GROUND_Y + 1), (SCREEN_WIDTH, GROUND_Y + 1), 3)
    # marcas
    spacing = 40
    for i in range(-1, SCREEN_WIDTH // spacing + 2):
        x = (i * spacing + offset) % (spacing * 4)  # loop
        pygame.draw.rect(surface, DARK_GRAY, (x, GROUND_Y + 4, 10, 6))


def draw_text(surface, text, x, y, size=20, color=BLACK):
    """Dibuja texto en pantalla."""
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))


def main():
    """
    Función principal: maneja el bucle del juego, eventos, lógica y dibujo.
    """
    running = True
    dino = Dinosaur()
    obstacles = []
    spawn_timer = 0
    spawn_interval = 90  # frames entre apariciones (se reducirá con el tiempo)
    speed = 6
    score = 0
    best_score = load_best_score()
    ground_offset = 0
    game_over = False
    game_over_cooldown = 0  # pequeño delay antes de reiniciar
    # sonido (opcional): usa pygame.mixer si se desea (aquí evitamos dependencias de archivos)
    ducking = False

    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Guarda mejor puntaje antes de salir
                if score > best_score:
                    save_best_score(score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        dino.jump()
                    if event.key == pygame.K_DOWN:
                        ducking = True
                else:
                    # en estado game over: presiona R para reiniciar
                    if event.key == pygame.K_r:
                        # reiniciar variables
                        dino = Dinosaur()
                        obstacles = []
                        spawn_timer = 0
                        spawn_interval = 90
                        speed = 6
                        score = 0
                        ground_offset = 0
                        game_over = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    ducking = False

        if not game_over:
            # Lógica de juego
            dino.duck(ducking)
            dino.update()

            # actualizar y crear obstáculos
            spawn_timer += 1
            # cada tantos frames crea un obstáculo (probabilidad para pájaro o cactus)
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                kind = "cactus" if random.random() < 0.78 else "bird"
                # aparecer fuera de pantalla
                obstacle = Obstacle(SCREEN_WIDTH + 10, kind=kind, speed=speed)
                obstacles.append(obstacle)
                # baja el intervalo ligeramente para aumentar dificultad (hasta cierto límite)
                spawn_interval = max(50, int(spawn_interval * 0.985))

            # actualizar obstáculos y detectar colisiones
            for ob in obstacles[:]:
                ob.speed = speed
                ob.update()
                if ob.is_off_screen():
                    obstacles.remove(ob)

            # colisiones
            dino_rect = dino.get_rect()
            for ob in obstacles:
                if dino_rect.colliderect(ob.get_rect()):
                    game_over = True
                    game_over_cooldown = FPS * 0.3  # short pause
                    # actualizar mejor puntaje
                    if score > best_score:
                        best_score = score
                        save_best_score(best_score)
                    break

            # aumentar velocidad y score con el tiempo
            score += 1  # incremento por frame; más rápido = más puntos
            # aumentar velocidad gradualmente
            if score % 500 == 0:
                speed += 0.5

            # mover "suelo"
            ground_offset = (ground_offset - int(speed)) % 40

        else:
            # en game over: permitir que se vea un poco la colisión antes de aceptar reinicio
            if game_over_cooldown > 0:
                game_over_cooldown -= 1

        # --- DIBUJO ---
        SCREEN.fill((235, 235, 235))
        # fondo de cielo simple
        pygame.draw.rect(SCREEN, (235, 235, 235), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # dibujar dino y obstáculos
        dino.draw(SCREEN)
        for ob in obstacles:
            ob.draw(SCREEN)

        # dibujar suelo
        draw_ground(SCREEN, ground_offset)

        # HUD: score
        draw_text(SCREEN, f"Puntaje: {score}", SCREEN_WIDTH - 160, 10)
        draw_text(SCREEN, f"Mejor: {best_score}", SCREEN_WIDTH - 160, 35)

        if game_over:
            draw_text(SCREEN, "GAME OVER", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, size=28, color=(180, 0, 0))
            draw_text(SCREEN, "Presiona R para reiniciar", SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 10, size=18)

        pygame.display.flip()

    # Al salir: guardar mejor puntaje si corresponde
    if score > best_score:
        save_best_score(score)


if __name__ == "__main__":
    main()
