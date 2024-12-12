from .types import Position
from .util import distance
from jelka import Color
from jelka.path import Path


class Sphere:
    def __init__(self, center: Position, radius: float, color: Color = Color(255, 192, 203)):
        self.center = center
        self.radius = radius
        self.color: Color = color
        self.path = Path()
        self.path.add_position(center, 0.01)

    def is_inside(self, pt: Position) -> bool:
        return distance(self.center, pt) <= self.radius

    def update_pos(self, time: float):
        self.center = self.path.current_position(time)
        # print(self.center)
        return
