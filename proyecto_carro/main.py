import pygame
from utils.config_loader import load_config
from game.car import Car
from game.obstacle import Obstacle
from avl.avl_tree import AVLTree
from gui.window import run_game


def cargar_obstaculos_en_avl(obstacles):
    """
    Inserta los obstáculos cargados del JSON en un AVL y retorna el árbol.
    """
    tree = AVLTree()
    for obs in obstacles:
        ob = Obstacle(obs["x"], obs["y"], obs["type"], obs.get("damage", 10))
        tree.root = tree.insert(tree.root, (ob.x, ob.y), ob)
    return tree


def main():
    # 1. Cargar configuración y obstáculos
    game_config, obstacles, obstacle_types = load_config("Config.json")

    # 2. Crear el carro y el árbol de obstáculos
    car = Car(50, 300)
    tree = cargar_obstaculos_en_avl(obstacles)

    # 3. Ejecutar el juego (pasamos el diccionario completo con "game")
    run_game(car, tree, {"game": game_config})


if __name__ == "__main__":
    main()
