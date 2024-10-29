import pygame
from config import *


class LifeBoost:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/health.png')
        self.image = pygame.transform.scale(self.image, (OBJECT_WIDTH, OBJECT_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    

    