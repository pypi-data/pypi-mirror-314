from jelka import Jelka, Color
import math
from jelka.util import distance


def callback(jelka: Jelka):
    global col
    if jelka.frame % 10 == 0:
        col = Color.vivid(Color.random_color())

    sphere_center = (0.25, 0.25, 0.5)
    rad2 = (math.e ** (math.sin(jelka.frame / 10))) / 3
    rad1 = (math.e ** (math.cos(jelka.frame / 10))) / 3

    cnt = 0
    for i in range(0, len(jelka.lights)):
        pos = jelka.positions_normalized[i]
        dist = distance(sphere_center, pos)
        if rad1 >= dist and dist >= rad2:
            cnt += 1
            j = dist / rad1
            if jelka.lights[i] == Color(0, 0, 0):
                jelka.set_light(i, Color(j * col.r, j * col.g, j * col.b))
            else:
                jelka.set_light(i, Color(j * jelka.lights[i].r, j * jelka.lights[i].g, j * jelka.lights[i].b))
        else:
            jelka.set_light(i, Color(0, 0, 0))
    if cnt == 0:
        jelka.frame += 2


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback)


main()
