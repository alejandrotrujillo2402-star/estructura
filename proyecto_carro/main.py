from utils.config_loader import load_config
from avl.avl_tree import AVLTree
from game.obstacle import Obstacle
from game.car import Car
from gui.window import run_game, generate_obstacles_random  


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
