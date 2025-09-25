# gui/window.py
import pygame
import time
import random
from avl.avl_tree import AVLTree  # asumes que ya existe la clase con insert + search_range
from gui.draw_utils import draw_obstacle  # usa tu función que dibuja según offset_x
from game.car import Car
from game.obstacle import Obstacle

# Evento para mover la "pantalla" cada refresh_time ms
MOVE_EVENT = pygame.USEREVENT + 1

def run_game(car: Car, tree: AVLTree, config: dict):
    pygame.init()
    SCREEN_W, SCREEN_H = 800, 600
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Juego Carrito con AVL")
    clock = pygame.time.Clock()

    # config
    refresh_ms = int(config["game"].get("refresh_time", 200))  # ms
    speed = config["game"].get("speed", 5)                     # unidades por MOVE_EVENT
    road_length = config["game"].get("road_length", 2000)
    screen_width = SCREEN_W

    # inicializar timer que mueve la pantalla/carrito cada refresh_ms
    pygame.time.set_timer(MOVE_EVENT, refresh_ms)

    offset_x = 0  # cuánto ha avanzado la carretera (en las mismas unidades que x de obstáculos)
    running = True

    # utilidad para marcar obstáculo como 'inactivo' tras colisión
    # (si prefieres eliminar del AVL, en lugar de marcar .active=False puedes llamar tree.delete(...))
    # asumimos que Obstacle tiene atributo .active (si no, lo añadimos al crear)

    while running:
        # 1) Procesar events (siempre hacerlo; si la ventana no tiene foco, clicarla)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOVE_EVENT:
                # avanzar la "cámara" / carretera cada refresh_ms
                offset_x += speed
                # comprobar meta
                if offset_x >= road_length:
                    print("¡Meta alcanzada!")
                    running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not car.is_jumping:
                    car.start_jump()      # implementar en tu clase Car
                if event.key == pygame.K_UP:
                    car.move_up = True
                if event.key == pygame.K_DOWN:
                    car.move_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    car.move_up = False
                if event.key == pygame.K_DOWN:
                    car.move_down = False

        # 2) Actualizaciones (cada frame)
        car.update()  # debe aplicar salto y devolver al color original al aterrizar

        # 3) Dibujo
        screen.fill((200, 200, 200))
        pygame.draw.line(screen, (0,0,0), (0, 340), (SCREEN_W, 340), 4)

        # dibujar carrito en su posición relativa
        car.draw(screen)

        # obtener obstáculos visibles según el AVL (x_min = offset_x, x_max = offset_x + screen_width)
        visible = tree.search_range(tree.root, offset_x, offset_x + screen_width)
        for obs in visible:
            if getattr(obs, "active", True):
                draw_obstacle(screen, obs, offset_x)

                # colisión: construir rects y comprobar colliderect
                obs_rect = pygame.Rect(obs.x - offset_x, 300 + obs.y*40, 40, 40)
                car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
                if car_rect.colliderect(obs_rect):
                    # aplicar daño sólo una vez
                    if getattr(obs, "active", True):
                        car.energy -= obs.damage
                        obs.active = False
                        print(f"Golpeado por {obs.type} -> energía {car.energy}")
                        # opcional: eliminar del árbol (necesitas implementar delete)
                        # tree.root = tree.delete(tree.root, (obs.x, obs.y))

                        # terminar si energía <= 0
                        if car.energy <= 0:
                            print("Carrito sin energía. Game over.")
                            running = False

        pygame.display.flip()
        # mantenemos un framerate alto para que las teclas se sientan responsivas
        clock.tick(60)

    pygame.quit()


# ------------------------------
# Generador simple de obstáculos
# ------------------------------
def generate_obstacles_random(n, road_length, lanes=(0,1,2), min_gap=40, start=200):
    """
    Genera lista de diccionarios de obstáculos con separación mínima `min_gap`.
    Úsalo para poblar tu config.json o insertar directamente en el AVL.
    """
    xs = []
    x = start
    for _ in range(n):
        x += random.randint(min_gap, min_gap + 120)
        if x > road_length: break
        xs.append(x)

    obs_list = []
    for x in xs:
        y = random.choice(lanes)
        typ = random.choice(["rock","hole"])  # o toma tipos del config
        obs_list.append({"x": x, "y": y, "type": typ})

    return obs_list
