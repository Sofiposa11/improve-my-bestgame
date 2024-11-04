import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class HealthItem:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/health.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x -= 5  # Velocidad del ítem de salud

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.health_items = []  # Lista para los ítems de salud
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        self.collision_count = 0
        self.max_collisions = 3
        self.score = 0  # Inicializamos la puntuación
        self.lives = 3  # Vidas iniciales del jugador

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

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        # Genera un nuevo obstáculo con una probabilidad
        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        # Genera un ítem de salud con una probabilidad
        if random.randint(0, 500) < 1:
            health_x = WIDTH
            health_y = random.randint(50, HEIGHT - 50)
            self.health_items.append(HealthItem(health_x, health_y))

        # Actualiza los obstáculos y los ítems de salud
        for obstacle in self.obstacles:
            obstacle.update()
        for item in self.health_items:
            item.update()

        # Filtra los obstáculos e ítems de salud que están fuera de la pantalla
        survived_obstacles = []
        survived_items = []
        player_rect = self.player.get_rect()

        for obstacle in self.obstacles:
            if obstacle.rect.x + obstacle.rect.width <= 0:  # Si el obstáculo salió de la pantalla
                self.score += 1  # Incrementa la puntuación al evitar un obstáculo
            elif player_rect.colliderect(obstacle.rect):  # Si el jugador colisiona
                self.lives -= 1
                self.collision_count += 1
                if self.lives <= 0:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
            else:
                survived_obstacles.append(obstacle)  # Si el obstáculo aún está en juego

        for item in self.health_items:
            if item.rect.x + item.rect.width > 0:
                if player_rect.colliderect(item.rect):  # Si el jugador recoge un ítem de salud
                    self.lives = min(self.lives + 1, 3)  # Máximo de 3 vidas
                else:
                    survived_items.append(item)

        self.obstacles = survived_obstacles
        self.health_items = survived_items

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for item in self.health_items:
            item.draw(self.screen)

        # Muestra la puntuación, el número de colisiones y las vidas
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30)
        self.draw_text(f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30)
        self.draw_text(f"Vidas: {self.lives}", font, BLACK, self.screen, 100, 70)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
