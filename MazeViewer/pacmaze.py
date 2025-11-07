import pygame
import sys
import json
import os
from pacman import PacMan
from pellet import Pellet

# chargement du labyrinthe depuis le JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "test_maze.json")
font_path = os.path.join(BASE_DIR, "font", "ARCADE_N.ttf")

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

#display score
font_score = pygame.font.Font(font_path, 20)

def draw_score(window, score):
    text = font_score.render(f"SCORE: {score}", True, (255, 255, 255))
    window.blit(text, (10, 10))


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

# retourne les positions valides pour les coins
def get_corner_positions(grid):
    corners = [
        (0, 0),
        (0, len(grid)-1),
        (len(grid[0])-1, 0),
        (len(grid[0])-1, len(grid)-1)
    ]
    valid_corners = []
    for x, y in corners:
        if grid[y][x] == 0:
            valid_corners.append((x, y))
        else:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == 0:
                        valid_corners.append((nx, ny))
                        break
    return valid_corners

# --> A UTILISER POURS LES PORTAILS <--
def get_portals(grid):
    portals = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 3:
                portals.append((x, y))
    return portals


def main():
    global pellets,score
    pacman = PacMan(grid, CELL_SIZE)
    corner_positions = get_corner_positions(grid)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:  # chemins
                pellets.append(Pellet(x, y, CELL_SIZE))
    # placer les power pellets dans les coins
    for x, y in corner_positions:
        pellets = [p for p in pellets if not (p.x == x and p.y == y)]
        pellets.append(Pellet(x, y, CELL_SIZE, is_power=True))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # inputs handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.set_direction(0, -1)
        elif keys[pygame.K_DOWN]:
            pacman.set_direction(0, 1)
        elif keys[pygame.K_LEFT]:
            pacman.set_direction(-1, 0)
        elif keys[pygame.K_RIGHT]:
            pacman.set_direction(1, 0)

        # déplacer pacman à chaque frame
        pacman.move()

        # pellet mangé ?
        for pellet in pellets:
            if not pellet.eaten and pellet.x == pacman.x and pellet.y == pacman.y:
                is_power = pellet.eat()
                score += 50 if is_power else 10
                if is_power:
                    pacman.activate_power(duration=50)
                    print("POWER MODE")
                print("SCORE -->" + str(score))


        window.fill(BLACK)
        draw_grid()
        pacman.draw(window)
        draw_score(window, score)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
