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
