import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30

        # Cargar imágenes
        self.image_normal = pygame.image.load(os.path.join(ASSETS_DIR, "car.png"))
        self.image_jump = pygame.image.load(os.path.join(ASSETS_DIR, "car_jump.png"))

        # Escalarlas al tamaño del carro
        self.image_normal = pygame.transform.scale(self.image_normal, (self.width, self.height))
        self.image_jump = pygame.transform.scale(self.image_jump, (self.width, self.height))

        # Estado inicial
        self.current_image = self.image_normal
        self.is_jumping = False
        self.jump_height = 80   # altura máxima
        self.jump_speed = 3
        self.jump_progress = 0
        self.energy = 100       # energía inicial
        self.move_up = False
        self.move_down = False

    def initialize_image(self):
        """Convierte las imágenes después de que la ventana esté creada"""
        self.image_normal = self.image_normal.convert_alpha()
        self.image_jump = self.image_jump.convert_alpha()
        self.current_image = self.image_normal

    def draw(self, surface):
        surface.blit(self.current_image, (self.x, self.y))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def start_jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.current_image = self.image_jump
            self.jump_progress = 0

    def update(self):
        """Actualizar estado del carro (salto, movimiento)"""
        if self.is_jumping:
            if self.jump_progress < self.jump_height:
                self.y -= self.jump_speed
                self.jump_progress += self.jump_speed
            else:
                self.y += self.jump_speed
                if self.y >= 300:  # posición base
                    self.y = 300
                    self.is_jumping = False
                    self.current_image = self.image_normal

        # Movimiento vertical (↑ ↓ opcional)
        if self.move_up and self.y > 200:
            self.y -= 5
        if self.move_down and self.y < 400:
            self.y += 5
