# gui/window.py
import pygame
import random
from gui.draw_utils import draw_obstacle
from avl.visualizer import draw_avl
from game.car import Car
from game.obstacle import Obstacle
from avl.avl_tree import AVLTree

MOVE_EVENT = pygame.USEREVENT + 1


def generate_obstacles_random(n, road_length, lanes=(0, 1, 2), min_gap=40, start=200):
    """
    Genera lista de obstáculos espaciados aleatoriamente.
    Retorna una lista de diccionarios que luego se insertan en el AVL.
    """
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
    """
    Devuelve el objeto Obstacle visible cuya posición en pantalla esté más cerca del carro.
    """
    visible = tree.search_range(tree.root, offset_x, offset_x + screen_width)
    if not visible:
        return None
    # distancia en pantalla (o.x - offset_x) comparada con car.x
    nearest = min(visible, key=lambda o: abs((o.x - offset_x) - car.x))
    return nearest


def run_game(car: Car, tree: AVLTree, config: dict):
    pygame.init()
    SCREEN_W, SCREEN_H = 1200, 600   # ancho mayor para ver el árbol al lado
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Juego Carrito con AVL")
    clock = pygame.time.Clock()

    refresh_ms = int(config["game"].get("refresh_time", 200))
    speed = config["game"].get("speed", 5)
    road_length = config["game"].get("road_length", 2000)
    screen_width = 800   # área del juego (izquierda)
    avl_width = 400      # área del AVL (derecha)

    pygame.time.set_timer(MOVE_EVENT, refresh_ms)

    offset_x = 0
    running = True

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
                    # (opcional) puedes insertar dummy para ver rebalanceo si quieres:
                    # dummy_obs = Obstacle(offset_x + random.randint(20, 50), 0, "jump", 0)
                    # tree.root = tree.insert(tree.root, (dummy_obs.x, dummy_obs.y), dummy_obs)

                # MOVER ARRIBA
                elif event.key == pygame.K_UP:
                    car.move_up = True

                # MOVER ABAJO
                elif event.key == pygame.K_DOWN:
                    car.move_down = True

                # INSERTAR DUMMY (ver rebalanceo)
                elif event.key == pygame.K_j:
                    dummy_obs = Obstacle(offset_x + random.randint(50, 200),
                                         random.choice([0, 1, 2]),
                                         "rock", 0)
                    tree.root = tree.insert(tree.root, (dummy_obs.x, dummy_obs.y), dummy_obs)
                    print(f"[J] Insertado dummy: {dummy_obs}")

                # ELIMINAR obstáculo visible más cercano
                elif event.key == pygame.K_k:
                    target = find_nearest_visible_obstacle(tree, offset_x, screen_width, car)
                    if target:
                        key = (target.x, target.y)
                        tree.root = tree.delete(tree.root, key)
                        print(f"[K] Eliminado obstáculo {key}")
                    else:
                        print("[K] No hay obstáculos visibles para eliminar.")

                # Mostrar AVL en una ventana matplotlib alternativa (opcional)
                elif event.key == pygame.K_t:
                    # show in separate window if avl.visualizer has such function
                    try:
                        from avl.visualizer import show_avl
                        show_avl(tree.root)
                    except Exception:
                        # silent fail if not available
                        pass

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    car.move_up = False
                elif event.key == pygame.K_DOWN:
                    car.move_down = False

        # --------------------
        # Actualizaciones
        # --------------------
        car.update()

        # --------------------
        # Área de juego (izquierda)
        # --------------------
        screen.fill((200, 200, 200), (0, 0, screen_width, SCREEN_H))
        pygame.draw.line(screen, (0, 0, 0), (0, 340), (screen_width, 340), 4)
        car.draw(screen)

        visible = tree.search_range(tree.root, offset_x, offset_x + screen_width)
        for obs in visible:
            if getattr(obs, "active", True):
                draw_obstacle(screen, obs, offset_x)

                obs_rect = pygame.Rect(obs.x - offset_x, 300 + obs.y * 40, 40, 40)
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

print("No hay obstáculos visibles para eliminar con K.")