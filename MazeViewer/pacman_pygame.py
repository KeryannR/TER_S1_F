import pygame
import sys
import json

# chargement du labyrinthe depuis le JSON
with open("test_maze.json", "r") as f:
    data = json.load(f)

grid = data["grid"]

# couleurs
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# dimensions du labyrinthe
ROWS = len(grid)
COLS = len(grid[0])

pygame.init()

# obtenir la taille de l’écran
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# marge autour du labyrinthe
MARGIN = 100

# calculer la taille max possible des cellules
max_cell_width = (SCREEN_WIDTH - MARGIN) // COLS
max_cell_height = (SCREEN_HEIGHT - MARGIN) // ROWS
CELL_SIZE = min(max_cell_width, max_cell_height)

# si le labyrinthe est encore trop grand, on impose un minimum
if CELL_SIZE < 2:
    CELL_SIZE = 2  # on évite des cases nulles

# calculer la taille finale de la fenêtre
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Labyrinthe PacMan")
clock = pygame.time.Clock()


def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:  # mur
                pygame.draw.rect(window, BLUE, rect)
            else: #chemin
                pygame.draw.rect(window, BLACK, rect)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)
        draw_grid()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
