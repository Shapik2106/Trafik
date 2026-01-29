# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import traffic
from graphs import open_graph_window

def start_gui():
    root = tk.Tk()
    root.title("Розрахунок характеристик телетрафіку")
    root.geometry("720x480")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")

    def calculate():
        try:
            N = float(ent_users.get())
            n = float(ent_sessions.get())
            t = float(ent_duration.get())
            T = float(ent_day.get())
            m = int(ent_channels.get())
            q = float(ent_recall.get()) / 100

            A, A1, Pc, Pb, Pa = traffic.calculate_traffic(N, n, t, T, m, q)

            lbl_A.config(text=f"{A:.3f}")
            lbl_A1.config(text=f"{A1:.3f}")
            lbl_Pc.config(text=f"{Pc:.3f}")
            lbl_Pb.config(text=f"{Pb:.3f}")
            lbl_Pa.config(text=f"{Pa:.3f}")

        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числові значення")

    main = ttk.Frame(root, padding=10)
    main.pack(fill="both", expand=True)

    input_f = ttk.LabelFrame(main, text="Вхідні параметри")
    input_f.grid(row=0, column=0, padx=10, pady=10)

    result_f = ttk.LabelFrame(main, text="Результати")
    result_f.grid(row=0, column=1, padx=10, pady=10)

    labels = [
        "Кількість абонентів",
        "Кількість сеансів",
        "Тривалість сеансу (с)",
        "Тривалість дня (хв)",
        "Кількість каналів",
        "Ймовірність передзвону (%)"
    ]

    defaults = ["1000", "20", "20", "1440", "5", "10"]
    entries = []

    for i, text in enumerate(labels):
        ttk.Label(input_f, text=text).grid(row=i, column=0, sticky="w", pady=3)
        e = ttk.Entry(input_f, width=20)
        e.grid(row=i, column=1, pady=3)
        e.insert(0, defaults[i])
        entries.append(e)

    (ent_users, ent_sessions, ent_duration,
     ent_day, ent_channels, ent_recall) = entries

    def r(row, txt):
        ttk.Label(result_f, text=txt).grid(row=row, column=0, sticky="w")
        lbl = ttk.Label(result_f, text="—", width=10)
        lbl.grid(row=row, column=1)
        return lbl

    lbl_A  = r(0, "Трафік A")
    lbl_A1 = r(1, "Трафік A₁")
    lbl_Pc = r(2, "Pc")
    lbl_Pb = r(3, "Pb")
    lbl_Pa = r(4, "Pa")

    btns = ttk.Frame(root)
    btns.pack(pady=10)

    ttk.Button(btns, text="Обчислити", command=calculate).grid(row=0, column=0, padx=10)
    ttk.Button(
        btns,
        text="Графіки",
        command=lambda: open_graph_window(
            ent_users.get(), ent_sessions.get(),
            ent_duration.get(), ent_day.get(),
            ent_channels.get(), ent_recall.get()
        )
    ).grid(row=0, column=1, padx=10)

    ttk.Button(btns, text="Вихід", command=root.destroy).grid(row=0, column=2, padx=10)

    root.mainloop()
