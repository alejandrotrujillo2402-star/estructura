import pygame
import random
import os
from gui.draw_utils import draw_obstacle
from avl.visualizer import draw_avl
from game.car import Car
from game.obstacle import Obstacle
from avl.avl_tree import AVLTree
from utils.config_loader import export_obstacles_to_json

MOVE_EVENT = pygame.USEREVENT + 1

# Cargar imagen de nube y sol
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
cloud_img = pygame.image.load(os.path.join(ASSETS_DIR, "nube.png"))
cloud_img = pygame.transform.scale(cloud_img, (80, 50))  # Escalar nube
sun_img = pygame.image.load(os.path.join(ASSETS_DIR, "sol.png"))
sun_img = pygame.transform.scale(sun_img, (60, 60))  # Escalar sol


def draw_road(screen, screen_width, screen_height, offset_x):
    """
    """
    # Colores
    GRASS_COLOR = (147, 197, 114)   
    ROAD_COLOR = (64, 64, 64)        # Gris oscuro para asfalto
    YELLOW_LINE = (255, 255, 0)      # Amarillo para líneas
    WHITE_LINE = (255, 255, 255)     # Blanco para bordes
    
    # Dimensiones de la carretera
    road_top = 280
    road_bottom = 420
    road_height = road_bottom - road_top
    
    # Dibujar césped arriba y abajo de la carretera
    pygame.draw.rect(screen, GRASS_COLOR, (0, 0, screen_width, road_top))
    pygame.draw.rect(screen, GRASS_COLOR, (0, road_bottom, screen_width, screen_height - road_bottom))
    
    # Dibujar asfalto de la carretera
    pygame.draw.rect(screen, ROAD_COLOR, (0, road_top, screen_width, road_height))
    
    # Dibujar líneas divisorias de carriles (líneas discontinuas amarillas)
    lane_width = road_height // 3
    # Primera línea divisoria
    y1 = road_top + lane_width
    # Segunda línea divisoria  
    y2 = road_top + 2 * lane_width
    
    # Líneas discontinuas amarillas para separar carriles
    dash_length = 30
    gap_length = 20
    for y_line in [y1, y2]:
        x = -(offset_x % (dash_length + gap_length))
        while x < screen_width:
            if x + dash_length > 0:  # Solo dibujar si es visible
                start_x = max(0, x)
                end_x = min(screen_width, x + dash_length)
                if end_x > start_x:
                    pygame.draw.line(screen, YELLOW_LINE, (start_x, y_line), (end_x, y_line), 3)
            x += dash_length + gap_length
    
    # Dibujar bordes blancos de la carretera
    pygame.draw.line(screen, WHITE_LINE, (0, road_top), (screen_width, road_top), 4)
    pygame.draw.line(screen, WHITE_LINE, (0, road_bottom), (screen_width, road_bottom), 4)
    
    # sol en la parte superior izquierda
    screen.blit(sun_img, (50, 30))
    
    # nubes estáticas 
    cloud_positions = [200, 400, 600, 800, 1000, 1200]  # Posiciones fijas de nubes
    for cloud_x in cloud_positions:
        if cloud_x > 0 and cloud_x < screen_width:  # Solo dibujar si está en pantalla
            cloud_y = 50  # Altura fija en el cielo
            screen.blit(cloud_img, (cloud_x, cloud_y))


def generate_obstacles_random(n, road_length, lanes=(0, 1, 2), min_gap=40, start=200):
    xs = []
    x = start
    for _ in range(n):
        x += random.randint(min_gap, min_gap + 120)
        if x > road_length:
            break
        xs.append(x)

    obs_list = []
    for x in xs:
        y = random.choice(lanes)
        typ = random.choice(["rock", "hole"])
        obs_list.append({"x": x, "y": y, "type": typ})

    return obs_list


def find_nearest_visible_obstacle(tree: AVLTree, offset_x: int, screen_width: int, car: Car):
    visible = tree.search_range(tree.root, offset_x, offset_x + screen_width)
    if not visible:
        return None
    nearest = min(visible, key=lambda o: abs((o.x - offset_x) - car.x))
    return nearest


def run_game(car: Car, tree: AVLTree, config: dict):
    pygame.init()
    SCREEN_W, SCREEN_H = 1200, 600
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Juego Carrito con AVL")
    clock = pygame.time.Clock()

    refresh_ms = int(config["game"].get("refresh_time", 200))
    speed = config["game"].get("speed", 5)
    road_length = config["game"].get("road_length", 2000)
    screen_width = 800
    avl_width = 400

    pygame.time.set_timer(MOVE_EVENT, refresh_ms)

    offset_x = 0
    running = True
    last_traversal_text = ""   # <- nuevo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOVE_EVENT:
                offset_x += speed
                if offset_x >= road_length:
                    print("¡Meta alcanzada!")
                    running = False

            elif event.type == pygame.KEYDOWN:
                # SALTO
                if event.key == pygame.K_SPACE and not car.is_jumping:
                    car.start_jump()

                # MOVER ARRIBA
                elif event.key == pygame.K_UP:
                    car.move_up = True

                # MOVER ABAJO
                elif event.key == pygame.K_DOWN:
                    car.move_down = True

                # INSERTAR DUMMY
                elif event.key == pygame.K_j:
                    dummy_obs = Obstacle(offset_x + random.randint(50, 200),
                                         random.choice([0, 1, 2]),
                                         "rock", 20)
                    tree.root = tree.insert(tree.root, (dummy_obs.x, dummy_obs.y), dummy_obs)
                    print(f"[J] Insertado dummy: {dummy_obs}")

                # ELIMINAR obstáculo
                elif event.key == pygame.K_k:
                    target = find_nearest_visible_obstacle(tree, offset_x, screen_width, car)
                    if target:
                        key = (target.x, target.y)
                        tree.root = tree.delete(tree.root, key)
                        print(f"[K] Eliminado obstáculo {key}")
                    else:
                        print("[K] No hay obstáculos visibles para eliminar.")

                # Mostrar AVL en ventana aparte
                elif event.key == pygame.K_t:
                    tree.highligth_nodes = True;
                    print("[T] Mostrando AVL en ventana del juego...")

                # Recorridos
                elif event.key == pygame.K_r:
                    result = tree.inorder(tree.root)
                    last_traversal_text = f"Inorder: {result}"
                    print(last_traversal_text)
                elif event.key == pygame.K_p:
                    result = tree.preorder(tree.root)
                    last_traversal_text = f"Preorder: {result}"
                    print(last_traversal_text)
                elif event.key == pygame.K_o:
                    result = tree.postorder(tree.root)
                    last_traversal_text = f"Postorder: {result}"
                    print(last_traversal_text)
                elif event.key == pygame.K_f:
                    result = tree.bfs()
                    last_traversal_text = f"BFS: {result}"
                    print(last_traversal_text)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    car.move_up = False
                elif event.key == pygame.K_DOWN:
                    car.move_down = False

     
        # Actualizaciones
        car.update()

        # --------------------
        # Área de juego (izquierda)
        # --------------------
        draw_road(screen, screen_width, SCREEN_H, offset_x)
        car.draw(screen)

        visible = tree.search_range(tree.root, offset_x, offset_x + screen_width)
        for obs in visible:
            if getattr(obs, "active", True):
                draw_obstacle(screen, obs, offset_x)

                # Ajustar la detección de colisiones para la nueva carretera
                road_top = 280
                road_bottom = 420
                lane_height = (road_bottom - road_top) // 3
                y_position = road_top + obs.y * lane_height + (lane_height - 40) // 2
                
                obs_rect = pygame.Rect(obs.x - offset_x, y_position, 40, 40)
                car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
                if car_rect.colliderect(obs_rect):
                    if getattr(obs, "active", True):
                        car.energy -= obs.damage
                        obs.active = False
                        print(f"Golpeado por {obs.type} -> energía {car.energy}")
                        if car.energy <= 0:
                            print("Carrito sin energía. Game over.")
                            running = False

        # --------------------
        # Área de AVL (derecha)
        # --------------------
        screen.fill((240, 240, 255), (screen_width, 0, avl_width, SCREEN_H))
        draw_avl(screen, tree, screen_width, 0, avl_width, SCREEN_H)

        # Mostrar recorrido seleccionado
        if last_traversal_text:
            font = pygame.font.SysFont(None, 20)
            wrapped = [last_traversal_text[i:i+40] for i in range(0, len(last_traversal_text), 40)]
            for i, line in enumerate(wrapped):
                text = font.render(line, True, (0, 0, 0))
                screen.blit(text, (screen_width + 10, 400 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    export_obstacles_to_json(tree)
