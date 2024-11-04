import pygame
from config import WIDTH

class RollingHeart:
    #Clase para los corazones rodantes que el jugador puede recolectar.
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)  # Tamaño del corazón
        self.image = pygame.image.load("assets/corazon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Redimensiona a 30x30
        self.speed = 5  # Velocidad de movimiento

    def update(self):
        #Actualiza la posición del corazón para que se mueva a la izquierda.
        self.rect.x -= self.speed

    def draw(self, surface):
        #Dibuja el corazón en la superficie dada.
        surface.blit(self.image, self.rect.topleft)
