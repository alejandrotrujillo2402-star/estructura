import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

class Car:
    def __init__(self, x, y, config=None):
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

        # Valores configurables desde JSON (con defaults)
        if config is None:
            config = {}
        game_cfg = config.get("game", {})

        self.jump_height = game_cfg.get("jump_height", 80)   # altura máxima
        self.jump_speed = game_cfg.get("jump_speed", 3)      # velocidad del salto
        self.energy = game_cfg.get("energy", 100)            # energía inicial
        self.base_y = y                                      # posición base en el suelo

        # Control de salto
        self.jump_progress = 0

        # Movimiento vertical
        self.move_up = False
        self.move_down = False

    def initialize_image(self):
        """Convierte las imágenes después de que la ventana esté creada"""
        self.image_normal = self.image_normal.convert_alpha()
        self.image_jump = self.image_jump.convert_alpha()
        self.current_image = self.image_normal

    def draw(self, surface):
        # Dibujar carro
        surface.blit(self.current_image, (self.x, self.y))

        # Dibujar barra de energía arriba del carro
        bar_width = self.width
        bar_height = 6
        bar_x = self.x
        bar_y = self.y - 10

        # proporción de energía (0-100)
        energy_ratio = max(self.energy, 0) / 100
        energy_color = (0, 200, 0) if self.energy > 30 else (200, 0, 0)

        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))   # fondo
        pygame.draw.rect(surface, energy_color, (bar_x, bar_y, int(bar_width * energy_ratio), bar_height))

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
                if self.y >= self.base_y:  # vuelve a posición base
                    self.y = self.base_y
                    self.is_jumping = False
                    self.current_image = self.image_normal

        # Movimiento vertical (↑ ↓ opcional, carriles)
        # Ajustado para la nueva carretera (280-420 px de altura)
        road_top = 280
        road_bottom = 420
        lane_height = (road_bottom - road_top) // 3
        
        if self.move_up and self.y > road_top:
            self.y -= 5
        if self.move_down and self.y < road_bottom - self.height:
            self.y += 5
