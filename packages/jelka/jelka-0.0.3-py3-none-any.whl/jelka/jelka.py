import os
import sys
import time
from typing import Callable, Dict, List

import jelka_validator.datawriter as dw

from .shapes import Shape
from .types import Color
from .types import Position


class Jelka:
    """Main class for controlling the tree."""

    def __init__(
        self,
        frame_rate: int = 60,
        initial_color: Color = Color(0, 0, 0),
        number_of_lights: int | None = None,
        custom_positions: str | None = None,
    ):
        self.frame_rate: int = frame_rate
        """Frame rate of the pattern."""

        self.frame: int = 0
        """Current frame number."""

        self.start_time: float = time.perf_counter()
        """Time when the pattern was started."""

        self.elapsed_time: float = 0.0
        """Time since the pattern was started."""

        self.positions_raw: Dict[int, Position] = dict()
        """Raw positions of the lights."""

        self.positions_normalized: Dict[int, Position] = dict()
        """Normalized positions of the lights."""

        self.center_raw: Position = Position(0, 0, 0)
        """Center of the tree in raw coordinates."""

        self.center_normalized: Position = Position(0, 0, 0)
        """Center of the tree in normalized coordinates."""

        # Provide default file locations
        filenames = [
            os.path.join(os.getcwd(), "positions.csv"),
            os.path.join(os.path.dirname(sys.argv[0]), "positions.csv"),
            os.path.join(os.getcwd(), "../data/positions.csv"),
            os.path.join(os.path.dirname(sys.argv[0]), "../data/positions.csv"),
        ]

        # Allow specifying a custom path
        if custom_positions:
            filenames = [custom_positions]

        # Try to load positions from various files
        self.load_positions(filenames)

        # Normalize the positions
        self.normalize_positions(0, 1)

        # Get max index of the lights
        if number_of_lights is None:
            number_of_lights = max(self.positions_raw.keys()) + 1

        self.number_of_lights: int = number_of_lights
        """Number of lights the pattern supports."""

        self.lights: List[Color] = [initial_color for _ in range(number_of_lights)]
        """List of colors of the lights."""

        self.objects: List["Shape"] = []
        """List of objects in the scene."""

        self.dw = dw.DataWriter(number_of_lights)
        """Direct access to the data writer."""

        self.clear = False
        """Whether to clear the lights before each frame."""

    def load_positions(self, filenames: List[str]):
        """Loads positions from the first available file."""

        for filename in filenames:
            if not os.path.isfile(filename):
                continue

            with open(filename) as file:
                print(f"Loading positions from {filename}", file=sys.stderr, flush=True)

                # Read the positions from the file
                for line in file.readlines():
                    line = line.strip()
                    if line == "":
                        continue
                    i, x, y, z = line.split(",")
                    self.positions_raw[int(i)] = Position(float(x), float(y), float(z))

                # Calculate the center of the tree
                minz = min([pos.z for pos in self.positions_raw.values()])
                maxz = max([pos.z for pos in self.positions_raw.values()])
                self.center_raw = Position(0, 0, (minz + maxz) / 2)

                return

        raise FileNotFoundError("No valid file found to load positions from")

    def normalize_positions(self, l: int = 0, r: int = 1, mn: "int | float | None" = None, mx: "int | float | None" = None):
        """Normalizes the positions to the range [l, r]."""

        if mn is None:
            mn = min([pos.x for pos in self.positions_raw.values()])
            mn = min(min([pos.y for pos in self.positions_raw.values()]), mn)
            mn = min(min([pos.z for pos in self.positions_raw.values()]), mn)

        if mx is None:
            mx = max([pos.x for pos in self.positions_raw.values()])
            mx = max(max([pos.y for pos in self.positions_raw.values()]), mx)
            mx = max(max([pos.z for pos in self.positions_raw.values()]), mx)
            mx += 0.01  # to avoid division by zero

        for i, pos in self.positions_raw.items():
            x = (pos.x - mn) / (mx - mn) * (r - l) + l
            y = (pos.y - mn) / (mx - mn) * (r - l) + l
            z = (pos.z - mn) / (mx - mn) * (r - l) + l
            self.positions_normalized[i] = Position(x, y, z)

        self.center_normalized = Position(
            (self.center_raw.x - mn) / (mx - mn) * (r - l) + l,
            (self.center_raw.y - mn) / (mx - mn) * (r - l) + l,
            (self.center_raw.z - mn) / (mx - mn) * (r - l) + l,
        )

    def set_light(self, i: int, color: Color):
        """Sets the color of the specified light."""
        self.lights[i] = color

    def run(self, callback: Callable[["Jelka"], None] | None = None, init: Callable[["Jelka"], None] | None = None):
        """Runs the main loop of the tree."""

        # Call the init function
        if init is not None:
            init(self)

        self.start_time = time.perf_counter()

        while True:
            self.elapsed_time = time.perf_counter() - self.start_time
            current_time = time.perf_counter()

            # Clear the lights if needed
            if self.clear:
                for light in range(self.number_of_lights):
                    self.set_light(light, Color(0, 0, 0))

            # Update the positions of the objects
            for obj in self.objects:
                obj.update_position(self.elapsed_time)

                for light, position in self.positions_normalized.items():
                    if obj.is_inside(position):
                        self.set_light(light, Color(obj.color.red, obj.color.green, obj.color.blue))

            # Call the callback function
            if callback is not None:
                callback(self)

            # Write the frame to the tree
            writable = [light.to_write() for light in self.lights]
            self.dw.write_frame(writable)

            new_time = time.perf_counter()
            frame_time = new_time - current_time
            self.frame += 1

            dt = 1.0 / self.frame_rate

            if frame_time <= dt:
                time.sleep(dt - frame_time)
            else:
                print("Warning: Cannot keep up with the frame rate", file=sys.stderr, flush=True)
                print(f"Frame time: {frame_time}, Max frame time: {dt}", file=sys.stderr, flush=True)
                pass
