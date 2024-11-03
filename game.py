import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2

        # Sistema de puntuación
        self.score = 0

        # Sistema de vidas
        self.lives_left = 3  # Número de vidas inicial

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        # Actualizar el fondo
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        # Generar obstáculos aleatoriamente
        if random.randint(0, 100) < 2:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Actualizar obstáculos
        for obstacle in self.obstacles:
            obstacle.update()

        # Eliminar obstáculos que han salido de la pantalla
        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        # Comprobar colisiones con obstáculos
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.lives_left -= 1  # Restar una vida
                self.obstacles.remove(obstacle)
                if self.lives_left <= 0:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

        # Incrementar puntuación
        self.score += 1  # Incrementa la puntuación en cada ciclo

    def draw(self):
        # Dibujar el fondo
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        # Dibujar el jugador
        self.player.draw(self.screen)

        # Dibujar los obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Mostrar la puntuación en pantalla
        self.draw_text(
            f"Puntuación: {self.score}", font, BLACK, self.screen, 150, 30
        )

        # Mostrar las vidas restantes en pantalla
        self.draw_text(
            f"Vidas: {self.lives_left}", font, BLACK, self.screen, WIDTH - 100, 30
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
