from ..types import Position


class Plane:
    def __init__(
        self,
        center: "Position | tuple[float, float, float]",
        normal: "Position | tuple[float, float, float]",
    ):
        self.center = Position(*center)
        self.normal = Position(*normal)
        self.d = self.center.dot(self.normal)
