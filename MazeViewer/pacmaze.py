import pygame
import sys
import json
import os
from pacman import PacMan
from pellet import Pellet
from ghost import Ghost

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

def draw_score(window, score, lives):
    # affiche le score
    text = font_score.render(f"SCORE: {score}", True, WHITE)
    window.blit(text, (10, 10))

    # affiche vies sous forme de cercles jaunes, sous le score
    life_y = 40
    circle_radius = 8
    circle_spacing = 25
    circle_x_start = 10

    for i in range(lives):
        center_x = circle_x_start + i * circle_spacing
        pygame.draw.circle(window, (255, 255, 0), (center_x, life_y), circle_radius)

# obtenir la taille de l'écran
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
lives = 3

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

def check_collisions(pacman, ghosts):
    global lives  # pour modifier la variable globale

    for ghost in ghosts:
        # collision directe
        if ghost.x == pacman.x and ghost.y == pacman.y:
            if pacman.power_mode:
                # Pac-Man mange le fantôme
                ghost.released = False
                ghost.release_timer = 100
                ghost.x, ghost.y = ghost.find_cage_position()
                ghost.prev_x, ghost.prev_y = ghost.x, ghost.y
                print(f"{ghost.color} mangé")
                continue
            else:
                lives -= 1
                print(f"Pac-Man touché -- Vies restantes : {lives}")
                pacman.reset_position()
                for ghost in ghosts:
                    ghost.reset_position()
                pygame.time.delay(1000)
                if lives <= 0:
                    print("############ GAME OVER ############")
                    return True  # fin du jeu
                return False  # Pac-Man continue

        # collision croisée
        if (getattr(ghost, "prev_x", None) == pacman.x and getattr(ghost, "prev_y", None) == pacman.y
            and ghost.x == getattr(pacman, "prev_x", None) and ghost.y == getattr(pacman, "prev_y", None)):
            if pacman.power_mode:
                ghost.released = False
                ghost.release_timer = 100
                ghost.x, ghost.y = ghost.find_cage_position()
                ghost.prev_x, ghost.prev_y = ghost.x, ghost.y
                print(f"{ghost.color} mangé (cross collision)")
                continue
            else:
                lives -= 1
                print(f"Pac-Man touché (cross collision) -- Vies restantes : {lives}")
                pacman.reset_position()
                for g in ghosts:
                    g.reset_position()
                if lives <= 0:
                    print("############ GAME OVER ############")
                    return True
                return False

    return False


def main():
    global pellets, score, lives
    score = 0
    lives = 3
    pellets = []

    pacman = PacMan(grid, CELL_SIZE)
    corner_positions = get_corner_positions(grid)
    ghosts = [Ghost(grid, CELL_SIZE, i) for i in range(4)]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:  # chemins
                pellets.append(Pellet(x, y, CELL_SIZE))
    # placer les power pellets dans les coins
    for x, y in corner_positions:
        pellets = [p for p in pellets if not (p.x == x and p.y == y)]
        pellets.append(Pellet(x, y, CELL_SIZE, is_power=True))

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        if not game_over:
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
            if not pacman.power_mode:
                for ghost in ghosts:
                    ghost.vulnerable = False

            for ghost in ghosts:
                ghost.move()

            if check_collisions(pacman, ghosts):
                game_over = True
                continue

            # pellet mangé ?
            for pellet in pellets:
                if not pellet.eaten and pellet.x == pacman.x and pellet.y == pacman.y:
                    is_power = pellet.eat()
                    score += 50 if is_power else 10

                    if is_power:
                        # mode power
                        pacman.activate_power(duration=200)  # 200 frames ≈ 20 sec à 10 FPS
                        print("POWER MODE")

                        # tous les fantômes deviennent vulnérables
                        for ghost in ghosts:
                            ghost.set_vulnerable(duration=200)

                    #print("SCORE -->" + str(score))


            window.fill(BLACK)
            draw_grid()
            pacman.draw(window)
            for ghost in ghosts:
                ghost.draw(window)
            draw_score(window, score, lives)
            pygame.display.flip()
            clock.tick(10)

        else:
            # --- ÉCRAN GAME OVER ---
            window.fill(BLACK)
            game_over_font = pygame.font.Font(font_path, 64)
            text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            window.blit(text, text_rect)

            small_font = pygame.font.Font(font_path, 24)
            info_text = small_font.render("Appuie sur ESPACE pour rejouer ou ESC pour quitter", True, WHITE)
            info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            window.blit(info_text, info_rect)

            score_text = small_font.render(f"Score final : {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
            window.blit(score_text, score_rect)

            pygame.display.flip()

            # gestion des événements sur l’écran Game Over
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            elif keys[pygame.K_SPACE]:
                # relance une nouvelle partie
                main()
                return
            clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
