from jelka import Jelka, Color


def callback(jelka: Jelka):
    if jelka.frame == 0:
        global col
        global spawnRate
        global lineLength
        col = Color.vivid(Color.random_color())
        spawnRate = 25
        lineLength = 10
        jelka.frame_rate = 8

    if (jelka.frame % spawnRate) < lineLength:
        jelka.set_light(0, color=col)
    else:
        jelka.set_light(0, color=Color(0, 0, 0))
        col = Color.vivid(Color.random_color())

    for i in reversed(range(1, jelka.n)):
        jelka.set_light(i, jelka.lights[i - 1])


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback)


main()
