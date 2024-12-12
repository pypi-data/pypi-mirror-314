from jelka import Jelka
from jelka.color import Color
import math


def callback(jelka: Jelka):
    for i in range(jelka.n):
        jelka.set_light(
            i,
            Color(
                (jelka.positions_normalized[i][0] * 255 + math.sin(jelka.elapsed_time + 1) * 255 + 256) % 256,
                (jelka.positions_normalized[i][1] * 255 + math.sin(jelka.elapsed_time + 2) * 255 + 256) % 256,
                (jelka.positions_normalized[i][2] * 255 + math.sin(jelka.elapsed_time) * 255 + 256) % 256,
            ).vivid(),
        )


def main():
    jelka = Jelka(300, 60, Color(255, 0, 0))
    jelka.run(callback)


main()
