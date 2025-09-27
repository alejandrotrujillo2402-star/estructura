class Obstacle:
    def __init__(self, x: int, y: int, type_: str, damage: int):
        self.x = x
        self.y = y
        self.type = type_
        self.damage = damage
        self.active = True  # usado para no chocar dos veces con el mismo obstáculo

    def __repr__(self):
        return f"Obstacle(x={self.x}, y={self.y}, type={self.type}, damage={self.damage})"
