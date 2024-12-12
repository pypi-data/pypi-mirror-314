from jelka import Jelka, Color
import math

axis = 2
threshold = 0.1


def callback(jelka: Jelka):
    if jelka.frame % 300 == 0:
        jelka.color = Color.random_color().vivid()

    coord = math.sin(jelka.frame / 80) / 1.8 + 0.55
    for i in range(jelka.n):
        jelka.set_light(i, jelka.color if abs(jelka.positions_normalized[i][axis] - coord) < threshold else jelka.color * 0.3)


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback)


main()
