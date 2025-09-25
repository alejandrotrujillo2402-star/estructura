class Obstacle:
    def __init__(self, x, y, type_, damage):
        self.x = x
        self.y = y
        self.type = type_
        self.damage = damage

    def __repr__(self):
        return f"Obstacle({self.x}, {self.y}, {self.type})"
