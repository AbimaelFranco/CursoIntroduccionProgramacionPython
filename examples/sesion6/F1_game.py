import pygame
import random
import sys
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evita los Bloques con Imagen")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PARTICLE_COLORS = [(255, 255, 50), (50, 255, 50), (255, 50, 255), (50, 255, 255)]
DEFAULT_BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 70, 200)
BUTTON_HOVER = (120, 120, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Ruta actual del script
current_dir = os.path.dirname(__file__)

# 🔹 Configuración de escalado
PLAYER_SCALE = 1.5       # factor de escala para el jugador (1.0 = tamaño original)
OBSTACLE_SCALE = 1     # factor de escala para obstáculos
DEBUG_MODE = True        # True = ver hitboxes, False = ocultar

# Tamaños máximos base
MAX_PLAYER_SIZE = 60
MAX_OBSTACLE_SIZE = 70

# Cargar imágenes
# Jugador
try:
    img = pygame.image.load(os.path.join(current_dir, "player.png")).convert_alpha()
    scale = min(MAX_PLAYER_SIZE / img.get_width(), MAX_PLAYER_SIZE / img.get_height(), 1)
    player_width = int(img.get_width() * scale * PLAYER_SCALE)
    player_height = int(img.get_height() * scale * PLAYER_SCALE)
    player_image = pygame.transform.scale(img, (player_width, player_height))
except:
    print("No se pudo cargar la imagen del jugador, usando rectángulo rojo.")
    player_image = None
    player_width = player_height = int(MAX_PLAYER_SIZE * PLAYER_SCALE)

# Obstáculo
try:
    img = pygame.image.load(os.path.join(current_dir, "obstacle.png")).convert_alpha()
    scale = min(MAX_OBSTACLE_SIZE / img.get_width(), MAX_OBSTACLE_SIZE / img.get_height(), 1)
    obstacle_width = int(img.get_width() * scale * OBSTACLE_SCALE)
    obstacle_height = int(img.get_height() * scale * OBSTACLE_SCALE)
    obstacle_image = pygame.transform.scale(img, (obstacle_width, obstacle_height))
except:
    print("No se pudo cargar la imagen del obstáculo, usando rectángulo azul.")
    obstacle_image = None
    obstacle_width = obstacle_height = int(MAX_OBSTACLE_SIZE * OBSTACLE_SCALE)

# Fondo
try:
    background_image = pygame.image.load(os.path.join(current_dir, "background.png")).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    print("No se pudo cargar el fondo, usando color sólido.")
    background_image = None

# Fuente
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# Funciones auxiliares
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_button(text, x, y, w, h, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    draw_text(text, font, WHITE, screen, x + w // 2, y + h // 2)
    return rect

# Juego principal
def game_loop():
    global player_width, player_height

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 20
    player_speed = 8

    obstacles = []
    particles = []
    score = 0
    frame_count = 0
    running = True

    def create_obstacle():
        x = random.randint(0, max(0, WIDTH - obstacle_width))
        y = -obstacle_height
        obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

    def create_particles(x, y):
        for _ in range(10):
            particles.append([[x, y], [random.uniform(-2, 2), random.uniform(-2, -5)], random.choice(PARTICLE_COLORS), random.randint(4, 6)])

    while running:
        # Fondo
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(DEFAULT_BG_COLOR)

        frame_count += 1
        mouse_pos = pygame.mouse.get_pos()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Velocidad de obstáculos según puntaje
        obstacle_speed = 6 + score // 5

        # Crear obstáculos
        if frame_count % 30 == 0:
            create_obstacle()

        # Hitbox del jugador
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Dibujar jugador
        if player_image:
            screen.blit(player_image, (player_x, player_y))
        else:
            pygame.draw.rect(screen, (255, 50, 50), player_rect)

        if DEBUG_MODE:
            pygame.draw.rect(screen, (0, 255, 0), player_rect, 2)

        # Mover y dibujar obstáculos
        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle_image:
                screen.blit(obstacle_image, (obstacle.x, obstacle.y))
            else:
                pygame.draw.rect(screen, (50, 200, 255), obstacle)

            if DEBUG_MODE:
                pygame.draw.rect(screen, (0, 255, 0), obstacle, 2)

            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                create_particles(obstacle.centerx, HEIGHT - 10)

        # Colisiones
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                running = False

        # Dibujar partículas
        for particle in particles[:]:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[3] -= 0.1
            pygame.draw.circle(screen, particle[2], (int(particle[0][0]), int(particle[0][1])), max(int(particle[3]), 0))
            if particle[3] <= 0:
                particles.remove(particle)

        # Puntaje
        draw_text(f"Puntaje: {score}", font, WHITE, screen, 80, 30)

        pygame.display.flip()
        clock.tick(FPS)

    game_over_loop(score)

# Game Over
def game_over_loop(score):
    while True:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(DEFAULT_BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        draw_text("GAME OVER", big_font, WHITE, screen, WIDTH//2, HEIGHT//3)
        draw_text(f"Puntaje: {score}", font, WHITE, screen, WIDTH//2, HEIGHT//3 + 60)

        play_button = draw_button("Jugar de nuevo", WIDTH//2 - 100, HEIGHT//2, 200, 50, mouse_pos)
        quit_button = draw_button("Salir", WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    game_loop()
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# Pantalla de inicio
def start_screen():
    while True:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(DEFAULT_BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        draw_text("EVITA LOS BLOQUES", big_font, WHITE, screen, WIDTH//2, HEIGHT//3)

        play_button = draw_button("Jugar", WIDTH//2 - 100, HEIGHT//2, 200, 50, mouse_pos)
        quit_button = draw_button("Salir", WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    game_loop()
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# Iniciar juego
start_screen()
