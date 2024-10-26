import pygame
from utils import load_spritesheet
from config import HEIGHT


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        # Cambié el código de los frames ya que este sprite viene con los frames por separado
        self.run_frames = self.run_frames = [pygame.image.load(f"assets/ninja/run/0{i}.png").convert_alpha() for i in range(10)]
        self.jump_frames = [pygame.image.load(f"assets/ninja/jump/{i}.png").convert_alpha() for i in range(5)]
        self.hit_frames = [pygame.image.load(f"assets/ninja/hit/{i}.png").convert_alpha() for i in range(4)]
        self.hit_frame_index = 0
        self.hit_animation_playing = False
        self.hit_animation_timer = 0
        self.frame_index = 0
        self.animation_speed = 0.3

    def collide(self):
        self.hit_animation_playing = True
        self.hit_frame_index = 0
        self.hit_animation_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        if self.hit_animation_playing:
            self.hit_animation_timer += 1
            if self.hit_animation_timer >= 10:
                self.hit_frame_index = (self.hit_frame_index + 1) % 4
                self.hit_animation_timer = 0
            if self.hit_frame_index == 3:  # Changed from 0 to 3
                self.hit_animation_playing = False
    
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, surface):

        if self.hit_animation_playing and self.hit_frames:
            frame = self.hit_frames[self.hit_frame_index]
            surface.blit(frame, (self.x, self.y))
        else:
            if self.on_ground:
                self.frame_index = (self.frame_index + self.animation_speed) % len(self.run_frames)
                frame = self.run_frames[int(self.frame_index)]
                surface.blit(frame, (self.x, self.y))
            else:
                frame = self.jump_frames[0]
                surface.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
