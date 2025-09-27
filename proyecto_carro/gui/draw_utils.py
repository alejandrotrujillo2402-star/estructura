import pygame
from game.obstacle import Obstacle

def draw_obstacle(screen, obstacle: Obstacle, offset_x: int):
    """
    Dibuja un obstáculo en pantalla según su posición y tipo.
    offset_x = cuánto ha avanzado la cámara (para simular movimiento).
    """
    rect = pygame.Rect(obstacle.x - offset_x, 300 + obstacle.y * 40, 40, 40)

    if obstacle.type == "rock":
        color = (150, 75, 0)   # marrón
    elif obstacle.type == "hole":
        color = (0, 0, 0)      # negro
    else:
        color = (255, 0, 0)    # rojo (default)

    pygame.draw.rect(screen, color, rect)
