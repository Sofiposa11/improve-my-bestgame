import pygame
import random

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  
        self.collected = False
        self.value = 1

    def update(self):
        self.rect.x -= 10  
        
    def draw(self, screen):
        
        pygame.draw.circle(screen, (255, 215, 0), self.rect.center, 10) 