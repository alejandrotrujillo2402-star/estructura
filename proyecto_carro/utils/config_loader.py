import json
import os
from game.obstacle import Obstacle

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_config(filename="Config.json"):
    full_path = os.path.join(BASE_DIR, filename)
    with open(full_path, "r") as f:
        config = json.load(f)

    game_config = config.get("game", {})
    obstacles_data = config.get("obstacles", [])
    obstacle_types = config.get("obstacle_damage", {})

    return game_config, obstacles_data, obstacle_types


def export_obstacles_to_json(tree, filename="Obstacles.json"):
    """
    Exporta los obstáculos activos del AVL a un archivo JSON.
    """
    obstacles = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        if getattr(node.data, "active", True):  # solo guardamos los activos
            obstacles.append({
                "x": node.data.x,
                "y": node.data.y,
                "type": node.data.type,
                "damage": node.data.damage
            })
        inorder(node.right)

    inorder(tree.root)

    full_path = os.path.join(BASE_DIR, filename)
    with open(full_path, "w") as f:
        json.dump({"obstacles": obstacles}, f, indent=2)

    print(f"[INFO] Obstáculos exportados a {full_path}")
