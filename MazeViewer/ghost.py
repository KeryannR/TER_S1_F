import pygame
import random

# Couleurs des fantômes
RED = (255, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
GHOST_COLORS = [RED, CYAN, PINK, ORANGE]

class Ghost:
    def __init__(self, grid, cell_size, ghost_index=0):
        self.grid = grid
        self.cell_size = cell_size
        self.ghost_index = ghost_index
        self.color = GHOST_COLORS[ghost_index % len(GHOST_COLORS)]
        self.x, self.y = self.find_cage_position()
        self.prev_x, self.prev_y = self.x, self.y
        self.start_x, self.start_y = self.x, self.y
        self.direction = (0, 0)
        self.move_delay = 3
        self.move_counter = 0

        self.vulnerable = False
        self.flash_timer = 0

        # --- Gestion de la sortie de la cage ---
        self.released = False
        self.release_timer = 30 + ghost_index * 50 

    ####### CAGE

    def find_cage_position(self):
        # listes cases #2
        cage_positions = [(x, y)
                        for y, row in enumerate(self.grid)
                        for x, cell in enumerate(row)
                        if cell == 2]

        # si cases #2
        if cage_positions:
            # si assez de positions pour indexer chaque fantôme
            if len(cage_positions) >= self.ghost_index + 1:
                return cage_positions[self.ghost_index]
            else:
                # sinon random
                return random.choice(cage_positions)

        # sinon 1ere case libre
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    return x, y


    def find_exit_from_cage(self):
        cage_positions = [(x, y)
                          for y, row in enumerate(self.grid)
                          for x, cell in enumerate(row)
                          if cell == 2]
        if not cage_positions:
            return self.x, self.y

        # on prend la case la plus haute de la cage
        top_cage_y = min(y for _, y in cage_positions)

        # cherche une case libre juste au-dessus
        for x, y in cage_positions:
            nx, ny = x, top_cage_y - 1
            if 0 <= ny < len(self.grid) and self.grid[ny][nx] == 0:
                return nx, ny

        # fallback : première case libre proche
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    if self.grid[ny][nx] == 0:
                        return nx, ny
        return self.x, self.y

    def reset_position(self):
        # revenir à la position de départ
        if hasattr(self, "start_x") and hasattr(self, "start_y"):
            self.x, self.y = self.start_x, self.start_y
        else:
            self.x, self.y = self.find_cage_position()

        # reset états internes
        self.prev_x, self.prev_y = self.x, self.y
        self.direction = (0, 0)
        self.released = False
        self.move_counter = 0

        # redémarre le timer de sortie de la cage
        self.release_timer = 30 + random.randint(0, 50)


    def can_move(self, x, y):
        # peut se déplacer sur cases 0 et 2 pour sortir 
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x] in [0, 2]
        return False

    def get_possible_directions(self):
        directions = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = self.x + dx, self.y + dy
            if self.can_move(nx, ny):
                directions.append((dx, dy))
        return directions

    def set_vulnerable(self, duration=200):
        self.vulnerable = True
        self.flash_timer = duration


    # DEPLACEMENT ALEATOIRE POUR L'INSTANT
    def move(self):
        self.prev_x, self.prev_y = self.x, self.y

        if self.vulnerable:
                self.flash_timer -= 1
                if self.flash_timer <= 0:
                    self.vulnerable = False

        if not self.released:
            self.release_timer -= 1
            if self.release_timer <= 0:
                # sortir vers l'extérieur de la cage
                self.released = True
                self.x, self.y = self.find_exit_from_cage()
                self.prev_x, self.prev_y = self.x, self.y
                self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            return

        # Mouvement aléatoire une fois sorti
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0

        nx, ny = self.x + self.direction[0], self.y + self.direction[1]
        if not self.can_move(nx, ny) or random.random() < 0.1:
            directions = self.get_possible_directions()
            if directions:
                self.direction = random.choice(directions)

        nx, ny = self.x + self.direction[0], self.y + self.direction[1]
        if self.can_move(nx, ny):
            self.x, self.y = nx, ny

    def draw(self, window, power_mode=False):
        size = int(self.cell_size * 0.7)
        offset = (self.cell_size - size) // 2
        rect = pygame.Rect(
            self.x * self.cell_size + offset,
            self.y * self.cell_size + offset,
            size,
            size
        )

        # Couleur selon l'état
        if self.vulnerable:
            # Si le temps est presque écoulé, clignote entre bleu et blanc
            if self.flash_timer < 60 and (self.flash_timer // 10) % 2 == 0:
                color = (255, 255, 255)  # blanc
            else:
                color = (0, 0, 255)  # bleu
        else:
            color = self.color  # couleur d'origine

        pygame.draw.rect(window, color, rect, border_radius=4)


