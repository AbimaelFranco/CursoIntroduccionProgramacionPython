import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evita los Bloques Vistoso")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (255, 50, 50)
OBSTACLE_COLOR = (50, 200, 255)
PARTICLE_COLORS = [(255, 255, 50), (50, 255, 50), (255, 50, 255), (50, 255, 255)]

# Clock
clock = pygame.time.Clock()
FPS = 60

# Jugador
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# Obstáculos
obstacle_width = 70
obstacle_height = 20
obstacle_speed = 6
obstacles = []

# Partículas
particles = []

# Puntaje
score = 0
font = pygame.font.SysFont("Arial", 30)

# Función para crear obstáculos
def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

# Función para crear partículas
def create_particles(x, y):
    for _ in range(10):
        particles.append([[x, y], [random.uniform(-2, 2), random.uniform(-2, -5)], random.choice(PARTICLE_COLORS), random.randint(4, 6)])

# Bucle principal
frame_count = 0
running = True
while running:
    screen.fill(BLACK)
    frame_count += 1

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Crear obstáculos periódicamente
    if frame_count % 30 == 0:
        create_obstacle()

    # Mover y dibujar obstáculos
    for obstacle in obstacles[:]:
        obstacle.y += obstacle_speed
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)
            score += 1
            create_particles(obstacle.centerx, HEIGHT - 10)

    # Detectar colisiones
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            running = False

    # Dibujar jugador
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Dibujar partículas
    for particle in particles[:]:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[3] -= 0.1
        pygame.draw.circle(screen, particle[2], (int(particle[0][0]), int(particle[0][1])), int(particle[3]))
        if particle[3] <= 0:
            particles.remove(particle)

    # Dibujar puntaje
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
