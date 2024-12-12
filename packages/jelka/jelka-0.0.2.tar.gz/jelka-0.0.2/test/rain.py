from jelka import Jelka, Color
from jelka.sphere import Sphere
import random as r


def init(jelka: Jelka):
    jelka.clear = True
    for i in range(0, 10):
        jelka.objects.append(Sphere((0.5, 0.5, 1.2), 0.5, Color(2, 0, 121)))
        jelka.objects[-1].center = (0.5 + r.uniform(-0.2, 0.2), 0.5 + r.uniform(-0.2, 0.2), 1 + r.uniform(0.0, 1.0))
        jelka.objects[-1].radius = 0.1
        # sph[i].set_start(sph[i].get_center())
        jelka.objects[-1].path.add_position(jelka.objects[-1].center, 3 + r.uniform(-1.0, 1.0))
        jelka.objects[-1].path.add_position(
            (r.uniform(-1.0, 1.0), r.uniform(-1.0, 1.0), -0.5 + r.uniform(-2.0, 0.4)), 1 + r.uniform(-0.2, 0.2)
        )
        # sph[i].set_end((r.uniform(-1.0, 1.0), r.uniform(-1.0, 1.0), -0.5 + r.uniform(-2.0, 0.4)))
        # sph[i].set_end((0,0,0))
        # sph[i].set_speed(0.01)
    # jelka.objects.append(Sphere((0.5,0.5,0.5),0.5))


def callback(jelka: Jelka):
    return 0


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback, init)


main()
