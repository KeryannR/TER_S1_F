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
        self.color = GHOST_COLORS[ghost_index % len(GHOST_COLORS)]
        self.x, self.y = self.find_cage_position()
        self.direction = (0, 0)
        self.move_delay = 3
        self.move_counter = 0

        # --- Gestion de la sortie de la cage ---
        self.released = False
        self.release_timer = 30 + ghost_index * 50 

    ####### CAGE

    def find_cage_position(self):
        cage_positions = [(x, y)
                          for y, row in enumerate(self.grid)
                          for x, cell in enumerate(row)
                          if cell == 2]
        if not cage_positions:
            # fallback : premier chemin libre
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell == 0:
                        return x, y
        return random.choice(cage_positions)

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

    # DEPLACEMENT ALEATOIRE POUR L'INSTANT
    def move(self):
        if not self.released:
            self.release_timer -= 1
            if self.release_timer <= 0:
                # sortir vers l'extérieur de la cage
                self.released = True
                self.x, self.y = self.find_exit_from_cage()
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

    def draw(self, window):
        size = int(self.cell_size * 0.7)
        offset = (self.cell_size - size) // 2
        rect = pygame.Rect(
            self.x * self.cell_size + offset,
            self.y * self.cell_size + offset,
            size,
            size
        )
        pygame.draw.rect(window, self.color, rect, border_radius=4)
