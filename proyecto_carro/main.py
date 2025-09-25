from utils.config_loader import load_config
from avl.avl_tree import AVLTree
from game.obstacle import Obstacle
from game.car import Car
from gui.window import run_game

def main():
    config = load_config("config.json")

    # Crear AVL
    tree = AVLTree()
    for obs in config["obstacles"]:
        obstacle = Obstacle(obs["x"], obs["y"], obs["type"],
                            config["obstacle_damage"][obs["type"]])
        tree.root = tree.insert(tree.root, (obs["x"], obs["y"]), obstacle)

    # Crear carrito
    car = Car(50, 300, tuple(config["game"]["car_color"]))

    # Ejecutar juego
    run_game(car, tree, config)

if __name__ == "__main__":
    main()
