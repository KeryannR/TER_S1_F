import pygame

WHITE = (255, 255, 255)

class Pellet:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.radius = max(2, cell_size // 10)
        self.eaten = False  # True si mangé

    def draw(self, window):
        if not self.eaten:
            center_x = self.x * self.cell_size + self.cell_size // 2
            center_y = self.y * self.cell_size + self.cell_size // 2
            pygame.draw.circle(window, WHITE, (center_x, center_y), self.radius)

    def eat(self):
        self.eaten = True
