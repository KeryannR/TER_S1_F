import pygame

WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

class Pellet:
    def __init__(self, x, y, cell_size, is_power=False):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.is_power = is_power
        self.radius = max(2, cell_size // 10)
        if self.is_power:
            self.radius = max(4, cell_size // 3)
        self.eaten = False

    def draw(self, window):
        if self.eaten:
            return

        if self.is_power:
            # clignote toutes les 300 ms
            time = pygame.time.get_ticks()
            if (time // 300) % 2 == 0:
                color = ORANGE
            else:
                color = (255, 255, 255)
        else:
            color = WHITE

        center_x = self.x * self.cell_size + self.cell_size // 2
        center_y = self.y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(window, color, (center_x, center_y), self.radius)

    def eat(self):
        self.eaten = True
        return self.is_power
