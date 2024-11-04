import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle
from coin import Coin  

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        pygame.init()  
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
        #base de la puntuacion
        self.score = 0
        self.cleared_obstacles = {}

        #temporizador de obstáculos
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = 60
    
        # propiedades de la barra de vida
        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 200
        self.health_bar_height = 20
        

        # f.propiedades de las monedas
        self.coins = []
        self.coin_spawn_timer = 0
        self.coin_spawn_delay = 120  
        self.coin_score = 0 
        
       
        self.debug = True

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            
            self.screen.fill(WHITE)
            
           
            self.update()
            
            
            self.draw()
            
           
            self.draw_health_bar()
            
            
            pygame.display.flip()
        
        pygame.quit()

    def update(self):
        self.player.update()
        
        
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0
        
        # Generar obstáculos con temporizador
        self.obstacle_spawn_timer += random.randint(1,2)
        if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
           
            is_flying = random.random() < 0.3  
            
            
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 150 if is_flying else HEIGHT - 50
            
            # Crear nuevo obstáculo
            new_obstacle = Obstacle(obstacle_x, obstacle_y)
            self.obstacles.append(new_obstacle)
            
            # Reiniciar temporizador
            self.obstacle_spawn_timer = 0
        

        self.coin_spawn_timer += 1
        if self.coin_spawn_timer >= self.coin_spawn_delay:
            coin_x = WIDTH
            # Posición aleatoria de la moneda
            coin_y = random.randint(HEIGHT - 200, HEIGHT - 50)
            self.coins.append(Coin(coin_x, coin_y))
            self.coin_spawn_timer = 0
        
        if self.collision_count >= self.max_collisions:
                self.game_over()
        
        for coin in self.coins[:]:
            coin.update()
            # Verificar colisión con el jugador
            if self.player.get_rect().colliderect(coin.rect) and not coin.collected:
                self.coin_score += coin.value
                self.coins.remove(coin)
                
               
        
    
        self.coins = [coin for coin in self.coins if coin.rect.x + coin.rect.width > 0]
        for obstacle in self.obstacles[:]:  
            obstacle.update()

        
        # Comprobar colisiones
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles[:]:
            if player_rect.colliderect(obstacle.rect):
                
                self.collision_count += 1
                self.obstacles.remove(obstacle)
                self.current_health = max(0, self.current_health - 34)
               
            
            # Actualizar puntuación
            elif not hasattr(obstacle, 'cleared') or not obstacle.cleared:
                if obstacle.rect.right < player_rect.left:
                    self.score += 10
                    obstacle.cleared = True
                    
        
        
            self.obstacles = [
                obstacle
                for obstacle in self.obstacles
                if obstacle.rect.x + obstacle.rect.width > 0
            ]

    def draw(self):
        
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )
        
      
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
       #puntaje
        self.draw_text(
            f"Collisions: {self.collision_count}", font, BLACK, self.screen, 100, 30
        )
        self.draw_text(
            f"score: {self.score}", font, BLACK, self.screen, WIDTH - 150, 30
        )

    def draw_health_bar(self):
        try:
        
            x, y = 20, 60
            
            #Barra roja
            pygame.draw.rect(
                self.screen,
                (255, 0, 0), 
                (x, y, self.health_bar_length, self.health_bar_height)
            )
            
            # Barra verde (salud)
            if self.current_health > 0:
                current_health_width = int((self.current_health / self.max_health) * self.health_bar_length)
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0), 
                    (x, y, current_health_width, self.health_bar_height)
                )
            
            # Borde
            pygame.draw.rect(
                self.screen,
                BLACK,
                (x, y, self.health_bar_length, self.health_bar_height),2
            )
            
            
        
        except Exception as e:
            if self.debug:
                print(f"Error drawing health bar: {e}")

        
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Mostrar puntuación de monedas
        self.draw_text(
            f"Coins: {self.coin_score}", font, BLACK, self.screen, WIDTH - 150, 70
        )

    def game_over(self):
        self.draw_text(
            "¡You lose!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
        )
        self.draw_text(
            f"Final Score: {self.score}", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2 + 50
        )
        self.draw_text(
            f"Coins Earned: {self.coin_score}", font, BLACK, self.screen, WIDTH // 2, HEIGHT //2 + 100
        )



    
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)