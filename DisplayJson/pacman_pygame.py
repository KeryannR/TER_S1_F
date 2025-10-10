import pygame
import sys
import json

# chargement du labyrinthe depuis le JSON
with open("test_maze.json", "r") as f:
    data = json.load(f)

width = data["width"]
height = data["height"]
grid = data["grid"]
legend = data["legend"]

# couleurs
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

CELL_SIZE = 40

# dimensions de la fenêtre
ROWS = len(grid)
COLS = len(grid[0])
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Labyrinthe Pac-Man")

clock = pygame.time.Clock()

# dessine le labyrinthe
def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:  # wall
                pygame.draw.rect(window, BLUE, rect)
            else:  # path
                pygame.draw.rect(window, BLACK, rect)

# boucle principale
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
