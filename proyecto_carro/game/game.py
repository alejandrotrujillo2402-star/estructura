import pygame
from utils.config_loader import load_config
from avl.avl_tree import AVLTree
from game.obstacle import Obstacle
from game.car import Car
from gui.window import generate_obstacles_random


def run_game(car, tree, config):
    print("🎮 run_game ha iniciado correctamente")
    pygame.init()

    # Configuración de la ventana
    SCREEN_WIDTH = config["game"].get("screen_width", 800)
    SCREEN_HEIGHT = config["game"].get("screen_height", 600)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Juego del Carrito")

    # Inicializar imagen del carro después de crear la ventana
    car.initialize_image()
    clock = pygame.time.Clock()
    running = True

    # 🚗 Bucle principal del juego
    while running:
        clock.tick(60)  # 60 FPS

        # --- Manejo de eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Manejo de teclas presionadas ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move_left()
        if keys[pygame.K_RIGHT]:
            car.move_right()
        if keys[pygame.K_SPACE]:
            car.start_jump()

        # --- Actualizar lógica del juego ---
        car.update()

        # --- Dibujar en pantalla ---
        screen.fill((200, 200, 200))  # Fondo gris
        car.draw(screen)

        pygame.display.flip()

    print("👋 run_game terminó")
    pygame.quit()


def main():
    config = load_config("config.json")
    tree = AVLTree()

    # ⚡ Generar MUCHOS obstáculos
    obstacles_data = generate_obstacles_random(
        n=80,
        road_length=config["game"].get("road_length", 2000)
    )
    config["obstacles"] = obstacles_data

    for obs in obstacles_data:
        damage = config["obstacle_damage"].get(obs["type"], 10)
        obstacle = Obstacle(obs["x"], obs["y"], obs["type"], damage)
        tree.root = tree.insert(tree.root, (obs["x"], obs["y"]), obstacle)

 
    car = Car(50, 300)

    run_game(car, tree, config)


if __name__ == "__main__":
    main()
