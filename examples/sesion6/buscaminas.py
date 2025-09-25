import pygame
import random
import sys

# --- CONFIGURACIÓN BÁSICA ---
pygame.init()

# Dimensiones de la ventana del juego
WIDTH, HEIGHT = 600, 700  # 600 px para el tablero, 100 px extra para el menú
ROWS, COLS = 10, 10       # Número de filas y columnas del tablero
CELL_SIZE = WIDTH // COLS # Tamaño de cada celda (ancho del tablero dividido entre columnas)

# Configuración del juego
MINES_COUNT = 15          # Número de minas
FONT = pygame.font.SysFont("comicsans", 30)  # Fuente para mostrar texto
MENU_HEIGHT = HEIGHT - WIDTH  # Altura del menú inferior

# --- Colores en formato RGB ---
BG_COLOR = (30, 30, 30)            # Fondo
GRID_COLOR = (50, 50, 50)          # Líneas de la cuadrícula
CELL_COLOR = (200, 200, 200)       # Color de celda no revelada
REVEALED_COLOR = (170, 170, 170)   # Color de celda revelada
MINE_COLOR = (255, 0, 0)           # Color de mina
TEXT_COLOR = (0, 0, 0)             # Color del texto de los números
MENU_COLOR = (40, 40, 40)          # Fondo del menú
BUTTON_COLOR = (100, 100, 255)     # Botón reinicio
BUTTON_HOVER_COLOR = (150, 150, 255) # Botón reinicio cuando el mouse pasa encima

# --- FUNCIONES DEL JUEGO ---

def create_board(rows, cols, mines_count):
    """
    Crea el tablero con minas y números.
    - Se inicializa una matriz de ceros.
    - Se colocan minas aleatoriamente.
    - Se cuenta cuántas minas rodean cada celda.
    """
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Selecciona posiciones aleatorias para las minas
    mines = random.sample([(r, c) for r in range(rows) for c in range(cols)], mines_count)
    for r, c in mines:
        board[r][c] = 'M'  # Se marca con 'M' la mina
    
    # Para cada celda sin mina, contar minas alrededor
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'M':
                count = 0
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if board[nr][nc] == 'M':
                                count += 1
                board[r][c] = count

    # print(board)
    return board


def reveal_cell(board, revealed, r, c):
    """
    Revela una celda:
    - Si es un número distinto de 0, se muestra.
    - Si es 0 (vacía), revela también sus vecinas (recursividad).
    """
    if revealed[r][c]:
        return
    revealed[r][c] = True
    if board[r][c] == 0:  # Expansión automática si no hay minas alrededor
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if not revealed[nr][nc]:
                        reveal_cell(board, revealed, nr, nc)


def draw_board(screen, board, revealed):
    """
    Dibuja el tablero en pantalla:
    - Celdas ocultas
    - Celdas reveladas
    - Números o minas
    """
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if revealed[r][c]:  # Si la celda está revelada
                pygame.draw.rect(screen, REVEALED_COLOR, rect)
                if board[r][c] != 0 and board[r][c] != 'M':
                    # Mostrar número
                    text = FONT.render(str(board[r][c]), True, TEXT_COLOR)
                    screen.blit(text, (c*CELL_SIZE + CELL_SIZE//4, r*CELL_SIZE + CELL_SIZE//4))
                elif board[r][c] == 'M':
                    # Mostrar mina
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, CELL_SIZE//3)
            else:
                pygame.draw.rect(screen, CELL_COLOR, rect)  # Celda oculta
            
            # Dibujar borde de celda
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)


def draw_menu(screen, score):
    """
    Dibuja el menú inferior:
    - Puntuación
    - Botón de reinicio
    """
    menu_rect = pygame.Rect(0, WIDTH, WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, MENU_COLOR, menu_rect)

    # Mostrar puntuación
    score_text = FONT.render(f"Puntuación: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, WIDTH + 10))

    # Crear botón de reinicio
    button_rect = pygame.Rect(WIDTH - 150, WIDTH + 10, 140, 40)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    
    button_text = FONT.render("Reiniciar", True, (255,255,255))
    screen.blit(button_text, (WIDTH - 140, WIDTH + 15))
    
    return button_rect


def check_win(board, revealed):
    """
    Verifica si el jugador ha ganado:
    - Todas las celdas sin mina deben estar reveladas.
    """
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != 'M' and not revealed[r][c]:
                return False
    return True


# --- BUCLE PRINCIPAL ---
def main():
    # Crear ventana del juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Buscaminas")
    clock = pygame.time.Clock()

    # Estado inicial del juego
    board = create_board(ROWS, COLS, MINES_COUNT)
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    score = 0

    # Bucle principal (game loop)
    while True:
        screen.fill(BG_COLOR)
        
        # Dibujar tablero y menú
        draw_board(screen, board, revealed)
        button_rect = draw_menu(screen, score)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Clic cuando el juego está activo
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                if button_rect.collidepoint(event.pos):
                    # Reiniciar juego
                    board = create_board(ROWS, COLS, MINES_COUNT)
                    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                    game_over = False
                    score = 0
                elif y < WIDTH:  # Clic dentro del tablero
                    r, c = y // CELL_SIZE, x // CELL_SIZE
                    if board[r][c] == 'M':
                        revealed[r][c] = True
                        game_over = True
                    else:
                        reveal_cell(board, revealed, r, c)
                        score += 1
            
            # Clic cuando el juego terminó (Game Over o Win)
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if button_rect.collidepoint(event.pos):
                    # Reinicio desde Game Over
                    board = create_board(ROWS, COLS, MINES_COUNT)
                    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                    game_over = False
                    score = 0

        # Mostrar mensaje si ganó
        if check_win(board, revealed):
            win_text = FONT.render("¡Ganaste!", True, (0,255,0))
            screen.blit(win_text, (WIDTH//2 - 60, HEIGHT//2 - 20))
            game_over = True

        # Mostrar mensaje si perdió
        if game_over and not check_win(board, revealed):
            lose_text = FONT.render("¡Game Over!", True, (255,0,0))
            screen.blit(lose_text, (WIDTH//2 - 80, HEIGHT//2 - 20))

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(30)


# Ejecutar el juego
if __name__ == "__main__":
    main()
