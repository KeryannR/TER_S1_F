import pygame

YELLOW = (255, 255, 0)

class PacMan:
    def __init__(self, grid, cell_size):
        self.grid = grid
        self.cell_size = cell_size
        self.x, self.y = self.find_start_position()

    # ----> MODIFIER POUR FAIRE SPAWN EN DESSOUS DE CAGE FANTOMES
    def find_start_position(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    return x, y
        return 0, 0

    def can_move(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x] == 0  # 0 = chemin
        return False

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.can_move(new_x, new_y):
            self.x, self.y = new_x, new_y

    def draw(self, window):
        center_x = self.x * self.cell_size + self.cell_size // 2
        center_y = self.y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        pygame.draw.circle(window, YELLOW, (center_x, center_y), radius)
