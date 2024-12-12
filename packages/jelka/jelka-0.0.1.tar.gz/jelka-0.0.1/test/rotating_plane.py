import math
import random
from colorsys import hsv_to_rgb, rgb_to_hsv


from jelka import Jelka, Color
from jelka.plane import Plane


def init(jelka: Jelka):
    None


def callback(jelka: Jelka):
    plane = Plane((0.5, 0.5, 0.5), (math.sin(jelka.frame / 40), 0, math.cos(jelka.frame / 40)))
    threshold = 0.1
    global c1, c2

    if jelka.frame % 150 == 0:
        c1 = Color.vivid(Color.random_color())
        c1hsv = rgb_to_hsv(c1.r / 255.0, c1.g / 255.9, c1.g / 255.0)
        c2hsv = ((c1hsv[0] * 360 + random.randint(80, 280) % 360) / 360.0, c1hsv[1], c1hsv[2])
        conv = hsv_to_rgb(*c2hsv)
        c2 = Color.vivid(Color(conv[0] * 255, conv[1] * 255, conv[2] * 255))

    for i in range(jelka.n):
        pos = jelka.positions_normalized[i]
        dcrtica = pos[0] * plane.normal[0] + pos[1] * plane.normal[1] + pos[2] * plane.normal[2]
        if plane.d - threshold <= dcrtica <= plane.d + threshold:
            jelka.set_light(i, c1)
        else:
            jelka.set_light(i, c2)


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback, init)


main()
