import math
from .types import Position


def length(p: Position) -> float:
    """Calculates absolute value of a point."""
    return math.sqrt(sum(x**2 for x in p))


def distance(p1: Position, p2: Position) -> float:
    return length((p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]))
