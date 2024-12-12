from jelka import Jelka, Color
from jelka.sphere import Sphere
import math


def init(jelka: Jelka):
    global normalized
    normalized = [0] * jelka.n

    min_x = min([jelka.positions_raw[i][0] for i in range(jelka.n)])
    max_x = max([jelka.positions_raw[i][0] for i in range(jelka.n)])
    min_y = min([jelka.positions_raw[i][1] for i in range(jelka.n)])
    max_y = max([jelka.positions_raw[i][1] for i in range(jelka.n)])
    min_z = min([jelka.positions_raw[i][2] for i in range(jelka.n)])
    max_z = max([jelka.positions_raw[i][2] for i in range(jelka.n)])
    for i in range(len(normalized)):
        normalized[i] = (
            (jelka.positions_raw[i][0] - min_x) / (max_x - min_x + 0.01),
            (jelka.positions_raw[i][1] - min_y) / (max_y - min_y + 0.01),
            (jelka.positions_raw[i][2] - min_z) / (max_z - min_z + 0.01),
        )


def callback(jelka: Jelka):
    global col

    height = 1 - 0.0075 * (jelka.frame % 150)
    if height == 1:
        col = Color.vivid(Color.random_color())
    rad = 1 / 2 - height / 2
    x = 0.5 + rad * math.cos(height * 20)
    y = 0.5 + rad * math.sin(height * 20)

    sph = Sphere((x, y, height), 0.1)

    for i in range(len(jelka.lights)):
        pos = normalized[i]
        if sph.is_inside(pos):
            jelka.set_light(i, col)
        # else:
        #   jelka.set_light(i, Color(0, 0, 0))


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback, init)


main()
