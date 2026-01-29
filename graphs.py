# graphs.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import traffic

def open_graph_window(N, n, t, T, m, q):
    win = tk.Toplevel()
    win.title("Графіки")
    win.geometry("900x500")
    win.resizable(False, False)

    left = ttk.Frame(win, padding=10)
    left.pack(side="left", fill="both", expand=True)

    right = ttk.Frame(win, padding=10)
    right.pack(side="right", fill="y")

    # ====== ВИБІР ПАРАМЕТРА ======
    ttk.Label(right, text="Варійований параметр").pack(anchor="w")

    param = tk.StringVar(value="N")

    for text, val in [
        ("Кількість абонентів", "N"),
        ("Кількість сеансів", "n"),
        ("Тривалість сеансу", "t"),
        ("Кількість каналів", "m")
    ]:
        ttk.Radiobutton(right, text=text, variable=param, value=val).pack(anchor="w")

    ttk.Separator(right).pack(fill="x", pady=5)

    ttk.Label(right, text="Графічне представлення").pack(anchor="w")
    graph_type = tk.StringVar(value="A")

    for text, val in [
        ("Трафік багатоканальної системи", "A"),
        ("Трафік на канал", "A1"),
        ("Ймовірність затримки Pc", "Pc"),
        ("Ймовірність відмови Pb", "Pb"),
        ("Ймовірність відмови Pa", "Pa")
    ]:
        ttk.Radiobutton(right, text=text, variable=graph_type, value=val).pack(anchor="w")

    def plot():
        xs = range(1, 101)
        ys = []

        for x in xs:
            vals = {
                "N": (x*10, float(n), float(t), float(T), int(m), float(q)/100),
                "n": (float(N), x, float(t), float(T), int(m), float(q)/100),
                "t": (float(N), float(n), x, float(T), int(m), float(q)/100),
                "m": (float(N), float(n), float(t), float(T), x, float(q)/100)
            }[param.get()]

            A, A1, Pc, Pb, Pa = traffic.calculate_traffic(*vals)
            ys.append({"A": A, "A1": A1, "Pc": Pc, "Pb": Pb, "Pa": Pa}[graph_type.get()])

        plt.figure("Графік")
        plt.plot(xs, ys, "r")
        plt.grid(True)
        plt.show()

    ttk.Button(right, text="Побудувати", command=plot).pack(pady=10)
    ttk.Button(right, text="Назад", command=win.destroy).pack()
