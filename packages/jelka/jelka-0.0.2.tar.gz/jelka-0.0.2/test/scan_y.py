from jelka import Jelka, Color
import math

axis = 1
threshold = 0.2


def init(jelka: Jelka):
    mx = max([x for x in jelka.positions_raw[1]])
    mn = min([x for x in jelka.positions_raw[1]])
    jelka.normalize_positions(0, 1, mn, mx)


def callback(jelka: Jelka):
    if jelka.frame % 300 == 0:
        jelka.color = Color.random_color().vivid()

    coord = math.sin(jelka.frame / 20) / 1 + 0.55
    for i in range(jelka.n):
        jelka.set_light(i, jelka.color if abs(jelka.positions_normalized[i][axis] - coord) < threshold else jelka.color * 0.3)


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback, init)


main()
