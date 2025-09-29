class Obstacle:
    def __init__(self, x, y, type_, damage=10):
        self.x = x
        self.y = y
        self.type = type_
        self.damage = damage
        self.active = True 

    def __repr__(self):
        return f"Obstacle({self.type}, x={self.x}, y={self.y}, dmg={self.damage})"
