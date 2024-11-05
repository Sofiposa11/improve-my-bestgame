import pygame 
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):  # Cambié _init por __init_
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
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

        # Actualiza los obstáculos
        for obstacle in self.obstacles:
            obstacle.update()

        # Filtra los obstáculos que están fuera de la pantalla
        survived_obstacles = []
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

        self.obstacles = survived_obstacles

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Muestra la puntuación, el número de colisiones y las vidas
        self.draw_text(f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30)
        self.draw_text(f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30)
        self.draw_text(f"Vidas: {self.lives}", font, BLACK, self.screen, 100, 70)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
