import pygame

def draw_avl_node(screen, node, x, y, dx, dy, font, color=(100, 200, 255)):
    if node is None:
        return

    # Dibujar nodo
    pygame.draw.circle(screen, color, (x, y), 18)
    text = font.render(str(node.key[0]), True, (0, 0, 0))
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    # Dibujar conexiones + hijos
    if node.left:
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x - dx, y + dy), 2)
        draw_avl_node(screen, node.left, x - dx, y + dy, dx // 2, dy, font)
    if node.right:
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x + dx, y + dy), 2)
        draw_avl_node(screen, node.right, x + dx, y + dy, dx // 2, dy, font)


def draw_avl(screen, tree, start_x, start_y, width, height):
    """
    Dibuja el AVL dentro de Pygame en un área reservada.
    """
    if tree.root is None:
        return

    font = pygame.font.SysFont(None, 20)
    draw_avl_node(screen, tree.root, start_x + width // 2, start_y + 40, width // 4, 60, font)
