from .types import Position
from typing import List
import math


class Path:
    def __init__(self):
        self.positions: List[Position] = []
        self.durations: List[float] = []
        self.loop = True

    def add_position(self, position: Position, time: float):
        self.positions.append(position)
        self.durations.append(time)

    def current_position(self, time: float) -> Position:
        # print(self.durations)
        total = 0
        for i in range(len(self.durations)):
            total += self.durations[i]

        if self.loop:
            time = time - math.floor(time / total) * total
        for i in range(len(self.durations)):
            if time <= self.durations[i]:
                # linear interpolation between this and next position
                # do it component-wise
                t = time / self.durations[i]
                if i == len(self.positions) - 1:
                    return self.positions[i]
                return (
                    self.positions[i][0] + t * (self.positions[i + 1][0] - self.positions[i][0]),
                    self.positions[i][1] + t * (self.positions[i + 1][1] - self.positions[i][1]),
                    self.positions[i][2] + t * (self.positions[i + 1][2] - self.positions[i][2]),
                )
            time -= self.durations[i]
        return self.positions[-1]
