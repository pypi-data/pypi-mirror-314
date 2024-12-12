Position = tuple[float, float, float]


# define adding and subtracing of positions
def __add__(self, other: Position) -> Position:
    return (self[0] + other[0], self[1] + other[1], self[2] + other[2])


def __sub__(self, other: Position) -> Position:
    return (self[0] - other[0], self[1] - other[1], self[2] - other[2])
