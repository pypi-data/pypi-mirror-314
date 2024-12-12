from typing import Tuple
import random


class Color:
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other: "Color") -> "Color":
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other: "Color") -> "Color":
        return Color(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other: "Color") -> "Color":
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def __truediv__(self, other: "Color") -> "Color":
        return Color(self.r / other.r, self.g / other.g, self.b / other.b)

    def __mul__(self, other: float) -> "Color":
        return Color(self.r * other, self.g * other, self.b * other)

    def __truediv__(self, other: float) -> "Color":
        return Color(self.r / other, self.g / other, self.b / other)

    def __eq__(self, other: "Color") -> bool:
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def to_tuple(self) -> Tuple[float, float, float]:
        return self.r, self.g, self.b

    def to_list(self) -> Tuple[float, float, float]:
        return [self.r, self.g, self.b]

    def to_write(self) -> Tuple[int, int, int]:
        def round_clamp(value):
            return max(0, min(255, round(value)))

        return round_clamp(self.r), round_clamp(self.g), round_clamp(self.b)

    def vivid(self):
        """Makes color more vivid."""
        return Color.vivid(self)

    def random_color() -> "Color":
        return Color(random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

    def vivid(c: "Color") -> "Color":
        """Makes color more vivid."""
        min(c.r, c.g, c.b)
        if c.r <= c.g and c.r <= c.b:
            c.r = 0
        elif c.g <= c.r and c.g <= c.b:
            c.g = 0
        else:
            c.b = 0
        return c
