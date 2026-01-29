

def calculate_traffic(N, n, t, T, m, q):
    A = (N * n * t) / (T * 60)
    A1 = A / m
    Pc = A1 / (1 + A1)
    Pb = Pc * q
    Pa = Pb * 0.8
    return A, A1, Pc, Pb, Pa


def main():

    from gui import start_gui
    start_gui()


if __name__ == "__main__":
    main()
