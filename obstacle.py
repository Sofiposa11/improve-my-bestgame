import pygame
from config import PURPLE  # Cambiamos a PURPLE en vez de RED

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, PURPLE, self.rect)  # Cambiado a PURPLE

