import pygame
from config import RED

class Obstacle:
    def __init__(self, x, y, is_flying=False):
        self.rect = pygame.Rect(x, y, 70, 50) 
        self.is_flying = is_flying
        self.cleared = False
       

    def update(self):
        self.rect.x -= 10  # Velocidad de movimiento del obstáculo
        

    def draw(self, screen):
        color = (255, 0, 0) if self.is_flying else (255, 0, 0)  
        pygame.draw.rect(screen, color, self.rect)
