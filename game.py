import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

# Nueva clase para los objetos de vida
class LifeItem:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/life_item.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2  # Velocidad a la que se mueve hacia la izquierda

    def update(self):
        self.rect.x -= self.speed  # Mover hacia la izquierda

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.life_items = []  # Lista para almacenar los objetos de vida
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
        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Generar objetos de vida aleatoriamente
        if random.randint(0, 500) < 1:  # Menos frecuente que los obstáculos
            life_item_x = WIDTH
            life_item_y = random.randint(50, HEIGHT - 100)
            self.life_items.append(LifeItem(life_item_x, life_item_y))

        # Actualizar obstáculos
        for obstacle in self.obstacles:
            obstacle.update()

        # Actualizar objetos de vida
        for life_item in self.life_items:
            life_item.update()

        # Eliminar obstáculos que han salido de la pantalla
        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        # Eliminar objetos de vida que han salido de la pantalla
        self.life_items = [
            life_item
            for life_item in self.life_items
            if life_item.rect.x + life_item.rect.width > 0
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

        # Comprobar colisiones con objetos de vida
        for life_item in self.life_items:
            if player_rect.colliderect(life_item.rect):
                self.lives_left += 1  # Añadir una vida
                self.life_items.remove(life_item)

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

        # Dibujar los objetos de vida
        for life_item in self.life_items:
            life_item.draw(self.screen)

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
