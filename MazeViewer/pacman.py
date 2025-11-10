import pygame

YELLOW = (255, 255, 0)

class PacMan:
    def __init__(self, grid, cell_size):
        self.grid = grid
        self.cell_size = cell_size
        self.x, self.y = self.find_start_position()
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.power_mode = False
        self.power_timer = 0
        self.move_delay = 1.5
        self.move_counter = 0

    # ----> POSITION A AMELIORER : POSITION DE SPAWN PLUS PRECISE <----
    def find_start_position(self):
        # trouve toutes les lignes où il y a des 2
        cage_lines = []
        for y, row in enumerate(self.grid):
            if 2 in row:
                cage_lines.append(y)

        if cage_lines:
            # prend la dernière -> bas de la cage
            cage_y = cage_lines[-1]

            # trouve les colonnes x des 2 sur cette ligne
            x_positions = [x for x, cell in enumerate(self.grid[cage_y]) if cell == 2]
            if x_positions:
                # prend le centre horizontal de la cage
                x_center = sum(x_positions) // len(x_positions)
                spawn_y = cage_y + 1

                # verifie si la case sous le centre est libre
                if spawn_y < len(self.grid) and self.grid[spawn_y][x_center] == 0:
                    return x_center, spawn_y

                # sinon chercher un 0 le plus proche horizontalement
                if spawn_y < len(self.grid):
                    row_below = self.grid[spawn_y]
                    for offset in range(1, len(row_below)):
                        left = x_center - offset
                        right = x_center + offset
                        if left >= 0 and row_below[left] == 0:
                            return left, spawn_y
                        if right < len(row_below) and row_below[right] == 0:
                            return right, spawn_y

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    return x, y

        return 0, 0

    def can_move(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x] == 0  # 0 = chemin
        return False

    def activate_power(self, duration=50):  # durée en frames
        self.power_mode = True
        self.power_timer = duration

    def move(self):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0

        new_x = self.x + self.next_direction[0]
        new_y = self.y + self.next_direction[1]
        if self.can_move(new_x, new_y):
            self.direction = self.next_direction

        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if self.can_move(new_x, new_y):
            self.x, self.y = new_x, new_y

        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False

    def set_direction(self, dx, dy):
        self.next_direction = (dx, dy)


    def draw(self, window):
        center_x = self.x * self.cell_size + self.cell_size // 2
        center_y = self.y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        pygame.draw.circle(window, YELLOW, (center_x, center_y), radius)
