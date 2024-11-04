# game.py

import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK, PURPLE, RED
from player import Player
from obstacle import Obstacle
from rolling_heart import RollingHeart  # Importar la nueva clase

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.heart_items = []

        # Fondo
        self.background_image = pygame.image.load("assets/background1.jpeg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
        self.background_scroll = 0
        self.background_speed = 2

        # Cargar imagen de corazón para el HUD
        self.heart_icon = pygame.image.load("assets/corazon.png").convert_alpha()
        self.heart_icon = pygame.transform.scale(self.heart_icon, (30, 30))

        # Sistema de corazones
        self.hearts = 3
        self.max_hearts = 5

        # Puntaje
        self.score = 0
        self.time_elapsed = 0

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            # Control de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Incremento del tiempo y cálculo del puntaje
            self.time_elapsed += 1 / FPS
            if int(self.time_elapsed) >= 1:
                self.score += 50
                self.time_elapsed = 0

            # Actualización y renderizado del juego
            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        # Movimiento del fondo
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -WIDTH:
            self.background_scroll = 0

        # Generación aleatoria de obstáculos
        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Generación aleatoria de corazones rodantes
        if random.randint(0, 1000) < 5:
            heart_x = WIDTH
            heart_y = random.randint(HEIGHT // 2, HEIGHT - 100)
            self.heart_items.append(RollingHeart(heart_x, heart_y))

        # Actualización de obstáculos y corazones
        for obstacle in self.obstacles:
            obstacle.update()
        for heart in self.heart_items:
            heart.update()

        # Eliminación de obstáculos y corazones fuera de pantalla
        self.obstacles = [
            obstacle for obstacle in self.obstacles if obstacle.rect.x + obstacle.rect.width > 0
        ]
        self.heart_items = [
            heart for heart in self.heart_items if heart.rect.x + heart.rect.width > 0
        ]

        # Verificación de colisiones con obstáculos
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.hearts -= 1
                self.obstacles.remove(obstacle)
                if self.hearts <= 0:
                    self.game_over_screen()  # Llamar a la pantalla de fin de juego
                    pygame.quit()
                    sys.exit()

        # Verificación de colisiones con ítems de vida
        for heart in self.heart_items[:]:
            if player_rect.colliderect(heart.rect):
                if self.hearts < self.max_hearts:
                    self.hearts += 1
                self.heart_items.remove(heart)

    def draw(self):
        # Dibujar el fondo
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + WIDTH, 0),
        )

        # Dibujar al jugador, obstáculos y corazones
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for heart in self.heart_items:
            heart.draw(self.screen)

        # Dibujar los corazones en pantalla
        for i in range(self.hearts):
            self.screen.blit(self.heart_icon, (20 + i * 35, 20))

        # Mostrar el puntaje actual
        self.draw_text(
            f"Puntaje: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def game_over_screen(self):
        #Muestra la pantalla de fin de juego con una animación de texto.
        game_over_font = pygame.font.SysFont(None, 96)
        score_font = pygame.font.SysFont(None, 48)
        
        game_over_text = "¡Perdiste!"
        score_text = f"Puntaje final: {self.score}"

        # Crear ciclo de animación de texto
        for size in range(60, 120, 5):  # Incremento de tamaño
            # Fondo de pantalla
            self.screen.fill(WHITE)

            # Mostrar "¡Perdiste!" en aumento de tamaño
            animated_font = pygame.font.SysFont(None, size)
            self.draw_text(game_over_text, animated_font, RED, self.screen, WIDTH // 2, HEIGHT // 2 - 50)

            # Mostrar el puntaje final más pequeño y fijo
            self.draw_text(score_text, score_font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 + 50)

            pygame.display.flip()
            pygame.time.delay(100)

        pygame.time.wait(2000)
