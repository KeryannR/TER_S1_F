import pygame

class Fruit:
    #PROVISOIRE POUR DESSINER UNE CERISE
    def __init__(self, x, y, cell_size, fruit_type="cherry"):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.fruit_type = fruit_type
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 6000

        self.points_by_type = {
            "cherry": 100,
            "strawberry": 300,
            "orange": 500,
            "apple": 700,
        }

        self.points = self.points_by_type.get(fruit_type, 100)

        self.color = (255, 0, 0)

    def draw(self, window):
        cx = self.x * self.cell_size + self.cell_size // 2
        cy = self.y * self.cell_size + self.cell_size // 2

        r = int(self.cell_size * 0.25)
        offset = int(self.cell_size * 0.20)

        pygame.draw.line(window, (0, 180, 0), (cx, cy - offset), (cx - offset, cy - 2 * offset), 4)
        pygame.draw.line(window, (0, 180, 0), (cx, cy - offset), (cx + offset, cy - 2 * offset), 4)

        pygame.draw.circle(window, (255, 50, 50), (cx - offset, cy), r)
        pygame.draw.circle(window, (255, 50, 50), (cx + offset, cy), r)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration
