# draw_utils.py
import os
import pygame
from game.obstacle import Obstacle

# Ruta absoluta a la carpeta assets
BASE_DIR = os.path.dirname(os.path.dirname(__file__))   # sube desde /gui a /proyecto_carro
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

rock_img = pygame.image.load(os.path.join(ASSETS_DIR, "rock.png"))
hole_img = pygame.image.load(os.path.join(ASSETS_DIR, "hole.png"))

rock_img = pygame.transform.scale(rock_img, (40, 40))
hole_img = pygame.transform.scale(hole_img, (40, 40))


def draw_obstacle(screen, obstacle: Obstacle, offset_x: int):
    """
    Dibuja un obstáculo en pantalla con imagen.
    offset_x = cuánto ha avanzado la cámara (para simular movimiento).
    """
    # Nueva configuración de carretera
    road_top = 280
    road_bottom = 420
    lane_height = (road_bottom - road_top) // 3
    
    # Calcular posición Y basada en el carril (0, 1, 2)
    y_position = road_top + obstacle.y * lane_height + (lane_height - 40) // 2
    
    rect = pygame.Rect(obstacle.x - offset_x, y_position, 40, 40)

    if obstacle.type == "rock":
        screen.blit(rock_img, rect)
    elif obstacle.type == "hole":
        screen.blit(hole_img, rect)
    else:
        # Obstáculo desconocido → usar rectángulo rojo
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, rect)
