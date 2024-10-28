import pygame
from config import *



class Obstacle:
    def __init__(self, x, y):
        self.frames = [pygame.transform.scale(pygame.image.load(f"assets/obstacle/obs{i}.png").convert_alpha(), (60, 60)) for i in range(4)]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.frame_index = 0
        self.animation_speed = 0.2

    def update(self):
        self.rect.x -= self.speed
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
