# graphs.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import traffic


class GraphsPage(ttk.Frame):
    def __init__(self, parent, on_back, get_inputs):
        super().__init__(parent, padding=10)
        self.on_back = on_back
        self.get_inputs = get_inputs
        self._build_ui()

    def _build_ui(self):
        left = ttk.Frame(self, padding=10)
        left.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(self, padding=10)
        right.pack(side="right", fill="y")

        lf_param = ttk.LabelFrame(right, text="Варійований параметр", padding=10)
        lf_param.pack(fill="x")

        self.param = tk.StringVar(value="N")
        for text, val in [
            ("Кількість абонентів", "N"),
            ("Кількість сеансів зв’язку", "n"),
            ("Тривалість сеансу зв’язку", "t"),
            ("Тривалість робочого дня", "T"),
            ("Кількість каналів", "m"),
            ("Ймовірність передзвону", "q"),
        ]:
            ttk.Radiobutton(lf_param, text=text, variable=self.param, value=val).pack(anchor="w")

        lf_graph = ttk.LabelFrame(right, text="Графічне представлення", padding=10)
        lf_graph.pack(fill="x", pady=10)

        self.graph_type = tk.StringVar(value="A")
        for text, val in [
            ("Трафік багатоканальної системи", "A"),
            ("Трафік системи на канал", "A1"),
            ("Ймовірність затримки системи Pc", "Pc"),
            ("Ймовірність відмови системи Pb", "Pb"),
            ("Ймовірність відмови системи Pa", "Pa"),
        ]:
            ttk.Radiobutton(lf_graph, text=text, variable=self.graph_type, value=val).pack(anchor="w")

        self.fig = Figure(figsize=(7.5, 4.8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=left)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        ttk.Button(right, text="Побудувати", command=self.plot).pack(fill="x", pady=(0, 6))
        ttk.Button(right, text="Назад", command=self.on_back).pack(fill="x")

    def plot(self):
        N, n, t, T, m, q = self.get_inputs()

        Nf = float(N)
        nf = float(n)
        tf = float(t)
        Tf = float(T)
        mi = int(m)
        qf = float(q)  # у %, бо traffic.calculate_traffic очікує %

        xs = range(1, 101)
        ys = []

        for x in xs:
            # x — 1..100
            if self.param.get() == "N":
                args = (x * 10, nf, tf, Tf, mi, qf)
            elif self.param.get() == "n":
                args = (Nf, x, tf, Tf, mi, qf)
            elif self.param.get() == "t":
                args = (Nf, nf, x, Tf, mi, qf)
            elif self.param.get() == "T":
                args = (Nf, nf, tf, x, mi, qf)
            elif self.param.get() == "m":
                args = (Nf, nf, tf, Tf, x, qf)
            else:  # "q"
                args = (Nf, nf, tf, Tf, mi, x)

            A, A1, Pc, Pb, Pa = traffic.calculate_traffic(*args)
            val = {"A": A, "A1": A1, "Pc": Pc, "Pb": Pb, "Pa": Pa}[self.graph_type.get()]
            ys.append(val)

        self.ax.clear()
        self.ax.plot(list(xs), ys)
        self.ax.grid(True)
        self.canvas.draw()