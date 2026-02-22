# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import traffic
from graphs import GraphsPage


def start_gui():
    root = tk.Tk()
    root.title("TRAFIC — розрахунок характеристик телетрафіку")
    root.geometry("1100x620")
    root.minsize(1100, 620)

    style = ttk.Style()
    try:
        style.theme_use("classic")
    except tk.TclError:
        style.theme_use("clam")

    # ===== Головний контейнер =====
    container = ttk.Frame(root, padding=10)
    container.grid(row=0, column=0, sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # ---------------- СТОРІНКА 1 ----------------
    main_page = ttk.Frame(container)
    main_page.grid(row=0, column=0, sticky="nsew")

    def show_main():
        main_page.tkraise()

    def show_graphs():
        graphs_page.tkraise()

    main_page.columnconfigure(0, weight=1)
    main_page.columnconfigure(1, weight=0)
    main_page.rowconfigure(0, weight=0)
    main_page.rowconfigure(1, weight=1)

    # ===== Вхідні параметри =====
    input_f = ttk.LabelFrame(main_page, text="Вхідні параметри", padding=12)
    input_f.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

    input_f.columnconfigure(0, weight=1)
    input_f.columnconfigure(1, weight=0)

    labels = [
        "Кількість абонентів",
        "Кількість сеансів зв’язку",
        "Тривалість сеансу зв’язку (с)",
        "Тривалість робочого дня (хв)",
        "Кількість каналів",
        "Ймовірність передзвону (%)",
    ]
    defaults = ["1000", "20", "20", "1440", "5", "10"]
    entries = []

    for i, text in enumerate(labels):
        ttk.Label(input_f, text=text).grid(row=i, column=0, sticky="w", pady=7, padx=(6, 16))
        e = ttk.Entry(input_f, width=18)
        e.grid(row=i, column=1, sticky="e", pady=7, padx=(0, 10))
        e.insert(0, defaults[i])
        entries.append(e)

    (ent_users, ent_sessions, ent_duration, ent_day, ent_channels, ent_recall) = entries

    def get_inputs():
        return (
            ent_users.get(),
            ent_sessions.get(),
            ent_duration.get(),
            ent_day.get(),
            ent_channels.get(),
            ent_recall.get(),
        )

    # ===== Панель керування =====
    ctrl_f = ttk.LabelFrame(main_page, text="Керування", padding=12)
    ctrl_f.grid(row=0, column=1, sticky="ne", pady=(0, 10))

    BTN_W = 18

    def calculate():
        try:
            N = float(ent_users.get())
            n = float(ent_sessions.get())
            t = float(ent_duration.get())
            T = float(ent_day.get())
            m = int(ent_channels.get())
            q_percent = float(ent_recall.get())

            A, A1, Pc, Pb, Pa = traffic.calculate_traffic(N, n, t, T, m, q_percent)

            lbl_A_val.config(text=f"{A:.2f}")
            lbl_A1_val.config(text=f"{A1:.2f}")
            lbl_Pc_val.config(text=f"{Pc:.0f}%")
            lbl_Pb_val.config(text=f"{Pb:.1f}%")
            lbl_Pa_val.config(text=f"{Pa:.2f}%")

        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числові значення")

    def show_help():
        messagebox.showinfo(
            "Довідка",
            "1) Введіть параметри\n"
            "2) Натисніть «Обчислити»\n"
            "3) Для графіків — «Графіки»"
        )

    ttk.Button(ctrl_f, text="Обчислити", width=BTN_W, command=calculate).grid(row=0, column=0, pady=(0, 10))
    ttk.Button(ctrl_f, text="Графіки", width=BTN_W, command=show_graphs).grid(row=1, column=0, pady=(0, 10))
    ttk.Button(ctrl_f, text="Довідка", width=BTN_W, command=show_help).grid(row=2, column=0, pady=(0, 10))
    ttk.Button(ctrl_f, text="Вихід", width=BTN_W, command=root.destroy).grid(row=3, column=0)

    # ===== Результати =====
    result_f = ttk.LabelFrame(main_page, text="Результати", padding=12)
    result_f.grid(row=1, column=0, columnspan=2, sticky="nsew")

    result_f.columnconfigure(0, weight=1)
    result_f.columnconfigure(1, weight=0)

    def result_row(r, text):
        ttk.Label(result_f, text=text).grid(row=r, column=0, sticky="w", pady=8, padx=(6, 16))
        lbl = ttk.Label(result_f, text="—", width=12, anchor="e", font=("Consolas", 10, "bold"))
        lbl.grid(row=r, column=1, sticky="e", pady=8, padx=(0, 10))
        return lbl

    lbl_A_val  = result_row(0, "Трафік багатоканальної системи A")
    lbl_A1_val = result_row(1, "Трафік системи на канал A₁")
    lbl_Pc_val = result_row(2, "Ймовірність затримки системи Pc")
    lbl_Pb_val = result_row(3, "Ймовірність відмови системи Pb")
    lbl_Pa_val = result_row(4, "Ймовірність відмови системи Pa")

    # ---------------- СТОРІНКА 2 ----------------
    graphs_page = GraphsPage(container, on_back=show_main, get_inputs=get_inputs)
    graphs_page.grid(row=0, column=0, sticky="nsew")

    show_main()
    root.mainloop()