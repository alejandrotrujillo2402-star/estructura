import pygame

class Car:
    def __init__(self, x, y, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.color = color
        self.base_color = color  # guardar color original
        self.energy = 100

        # Movimiento vertical
        self.move_up = False
        self.move_down = False

        # Salto
        self.is_jumping = False
        self.jump_count = 10
        self.jump_color = (0, 255, 0)  # verde mientras salta

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def start_jump(self):
        """Inicia el salto si no está saltando ya"""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 10
            self.color = self.jump_color

    def update(self):
        """Actualiza movimiento vertical y salto"""
        # Movimiento simple arriba/abajo con teclas
        if self.move_up:
            self.y -= 5
        if self.move_down:
            self.y += 5

        # Lógica de salto
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                # efecto parabólico
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                # terminó el salto
                self.is_jumping = False
                self.jump_count = 10
                self.color = self.base_color
