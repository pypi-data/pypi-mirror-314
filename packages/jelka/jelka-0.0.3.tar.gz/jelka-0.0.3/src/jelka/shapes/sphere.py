from .path import Path
from .shape import Shape
from ..types import Color, Position
from ..util import distance


class Sphere(Shape):
    def __init__(
        self,
        center: "Position | tuple[float, float, float]",
        radius: float,
        color: Color = Color(255, 192, 203),
    ):
        self.center: Position = Position(*center)
        self.radius: float = radius
        self.color: Color = color

        self.path = Path()
        self.path.add_position(self.center, 0.01)

    def is_inside(self, position: Position) -> bool:
        return distance(self.center, position) <= self.radius

    def update_position(self, time: float):
        self.center = self.path.current_position(time)
