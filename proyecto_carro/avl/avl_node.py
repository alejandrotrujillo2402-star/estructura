# avl/avl_node.py
class AVLNode:
    def __init__(self, key, data=None):
        self.key = key      # tu clave: (x, y)
        self.data = data    # info del obstáculo (Objeto Obstacle)
        self.left = None
        self.right = None
        self.height = 1
