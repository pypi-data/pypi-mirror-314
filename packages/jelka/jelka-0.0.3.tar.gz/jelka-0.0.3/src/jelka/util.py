from .types import Position


def length(position: Position) -> float:
    """Calculates an absolute value of a point."""
    return position.magnitude()


def distance(p1: Position, p2: Position) -> float:
    """Calculates a distance between two points."""
    return (p1 - p2).magnitude()
