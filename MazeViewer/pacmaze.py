import pygame
import sys
import json
import os
from pacman import PacMan
from pellet import Pellet

# chargement du labyrinthe depuis le JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "test_maze.json")

with open(json_path, "r") as f:
    data = json.load(f)

grid = data["grid"]

# couleurs
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

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

pellets = []
score = 0

def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:  # mur
                pygame.draw.rect(window, BLUE, rect)
            else: #chemin
                pygame.draw.rect(window, BLACK, rect)
    for pellet in pellets:
        pellet.draw(window)

def main():
    global score
    pacman = PacMan(grid, CELL_SIZE)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:  # chemins
                pellets.append(Pellet(x, y, CELL_SIZE))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # inputs handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move(0, -1)
        elif keys[pygame.K_DOWN]:
            pacman.move(0, 1)
        elif keys[pygame.K_LEFT]:
            pacman.move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            pacman.move(1, 0)

        # pellet mangé ?
        for pellet in pellets:
            if not pellet.eaten and pellet.x == pacman.x and pellet.y == pacman.y:
                pellet.eat()
                score += 10
                print("SCORE -->" + str(score))


        window.fill(BLACK)
        draw_grid()
        pacman.draw(window)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
