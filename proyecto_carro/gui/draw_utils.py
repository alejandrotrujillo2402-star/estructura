import pygame

def draw_obstacle(screen, obstacle, offset_x):
    """Dibuja un obstáculo relativo al avance"""
    rect = pygame.Rect(obstacle.x - offset_x, 300 + obstacle.y*40, 40, 40)

    if obstacle.type == "rock":
        color = (150, 75, 0)   # marrón
    elif obstacle.type == "hole":
        color = (0, 0, 0)      # negro
    else:
        color = (255, 0, 0)    # rojo por defecto

    pygame.draw.rect(screen, color, rect)
