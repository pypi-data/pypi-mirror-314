from jelka import Jelka


def init(jelka: Jelka):
    None


def callback(jelka: Jelka):
    None


def main():
    jelka = Jelka(300, 60)
    jelka.run(callback, init)


main()
