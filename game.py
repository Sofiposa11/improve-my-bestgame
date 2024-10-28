import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle
from lifeboost import LifeBoost

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        # Cambié el fondo
        self.background_image = pygame.image.load("assets/def_bg.png")
        self.background_offset = 0
        # Se establece un límite de vidas
        self.lives = 10
        # Puntaje
        self.score = 0
        self.life_boosts = []
        self.font = pygame.font.SysFont(None, 48)
        self.last_score_increment = pygame.time.get_ticks()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()
        
        # Actualiza el fondo
        self.background_offset -= 1
        if self.background_offset < -WIDTH:
            self.background_offset = 0

        # Incrementar puntaje (1 punto cada medio segundo)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_increment >= 300:  # 300 milisegundos = 0.3 segundos
            self.score += 1
            self.last_score_increment = current_time

        if random.randint(0, 80) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        if self.score % 30 == 0 and len(self.life_boosts) == 0 and self.lives < 10:
            life_boost = LifeBoost(WIDTH, HEIGHT - 45)
            self.life_boosts.append(life_boost)

        for life_boost in self.life_boosts:
            life_boost.update()
            if life_boost.rect.colliderect(self.player.get_rect()):
                self.lives += 1
                self.life_boosts.remove(life_boost)
            if life_boost.rect.x < -life_boost.rect.width:
                self.life_boosts.remove(life_boost)

        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.obstacles.remove(obstacle)
                # La función de la animación se activa cuando colisiona con un obstáculo
                self.player.collide()
                # Se resta una vida cada que el personaje colisiona con un obstáculo
                self.lives -= 1
                if self.lives <= 0:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

    def draw(self, surface):
        
        # Cada capa se dibuja dos veces, una al lado de la otra, para que el efecto de scrolling sea más fluido. 
        surface.blit(self.background_image, (self.background_offset, 0))
        surface.blit(self.background_image, (self.background_offset + WIDTH, 0))

        self.player.draw(self.screen)

        self.draw_text(f"Puntuación: {self.score}", self.font, BLACK, self.screen, 650, 30)
        # Se muestra en pantalla cuantas vidas tiene el jugador
        self.draw_text( f"Vidas: {self.lives}", font, BLACK, self.screen, 90, 30)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for life_boost in self.life_boosts:
            life_boost.draw(self.screen)        
        

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)


