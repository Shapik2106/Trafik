# traffic.py
import math


def erlang_b_percent(y: float, L: int) -> float:
    """Pb у відсотках (Erlang B)."""
    numerator = (y ** L) / math.factorial(L)
    denominator = sum((y ** k) / math.factorial(k) for k in range(0, L + 1))
    return 100.0 * numerator / denominator


def calculate_traffic(N, n, t, T, m, q_percent):
    """
    Повертає:
      A, A1 - (Ерланги)
      Pc, Pb, Pa - у відсотках (%)
    """
    y = (float(N) * float(n) * float(t)) / (float(T) * 60.0)
    L = int(m)
    P0 = float(q_percent) / 100.0

    A = y
    A1 = y / L

    # Pb (Erlang B) у %
    Pb = erlang_b_percent(y, L)

    # Pc у %
    if y >= L:
        Pc = 100.0
    else:
        Pc = 100.0 * P0 * (y ** L) / (math.factorial(L - 1) * (L - y))
        Pc = min(Pc, 100.0)  # <-- ключове виправлення

    # Pa у % (як у твоїй формулі з методички)
    Pa = (
        100.0
        * y
        * (1.0 + 1.0 / (L + 1) + 1.0 / ((L + 1) * (L + 2)))
        / (math.factorial(L) * math.exp(y))
    )

    return A, A1, Pc, Pb, Pa