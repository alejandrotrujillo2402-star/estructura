class AVLNode:
    def __init__(self, key, data=None):
        self.key = key      # (x, y)
        self.data = data    # información extra del obstáculo
        self.left = None
        self.right = None
        self.height = 1
