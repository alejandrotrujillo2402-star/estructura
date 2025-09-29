import pygame

# --- Dibujo en Pygame (ya lo tenías) ---
def draw_avl_node(screen, node, x, y, dx, dy, font, color=(100, 200, 255)):
    if node is None:
        return
    pygame.draw.circle(screen, color, (x, y), 18)
    text = font.render(str(node.key[0]), True, (0, 0, 0))
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    if node.left:
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x - dx, y + dy), 2)
        draw_avl_node(screen, node.left, x - dx, y + dy, dx // 2, dy, font)
    if node.right:
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x + dx, y + dy), 2)
        draw_avl_node(screen, node.right, x + dx, y + dy, dx // 2, dy, font)

def draw_avl(screen, tree, start_x, start_y, width, height):
    if tree.root is None:
        return
    font = pygame.font.SysFont(None, 20)
    draw_avl_node(screen, tree.root, start_x + width // 2, start_y + 40, width // 4, 60, font)

# --- NUEVO: Mostrar AVL en una ventana aparte con matplotlib ---
import matplotlib.pyplot as plt
import networkx as nx

def show_avl(root):
    """Muestra el árbol AVL en una ventana nueva usando matplotlib + networkx"""
    if root is None:
        print("Árbol vacío")
        return

    G = nx.DiGraph()

    def add_edges(node):
        if not node:
            return
        G.add_node(str(node.key))
        if node.left:
            G.add_edge(str(node.key), str(node.left.key))
            add_edges(node.left)
        if node.right:
            G.add_edge(str(node.key), str(node.right.key))
            add_edges(node.right)

    add_edges(root)

    pos = nx.spring_layout(G)  # disposición automática
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Árbol AVL - Vista de Recorridos")
    plt.show()
