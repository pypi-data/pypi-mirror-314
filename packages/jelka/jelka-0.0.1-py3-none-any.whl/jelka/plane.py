from .types import Position


class Plane:
    def __init__(self, center: Position, normal: Position):
        self.center = center
        self.normal = normal
        self.d = normal[0] * center[0] + normal[1] * center[1] + normal[2] * center[2]
