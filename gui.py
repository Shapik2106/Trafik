# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import traffic

def calculate():
    try:
        N = float(ent_users.get())
        n = float(ent_sessions.get())
        t = float(ent_duration.get())
        T = float(ent_day.get())
        m = int(ent_channels.get())
        q = float(ent_recall.get()) / 100

        A, A1, Pc, Pb, Pa = traffic.calculate_traffic(N, n, t, T, m, q)

        lbl_A_val.config(text=f"{A:.3f}")
        lbl_A1_val.config(text=f"{A1:.3f}")
        lbl_Pc_val.config(text=f"{Pc:.3f}")
        lbl_Pb_val.config(text=f"{Pb:.3f}")
        lbl_Pa_val.config(text=f"{Pa:.3f}")

    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректні числові дані")

# ====== ВІКНО ======
root = tk.Tk()
root.title("Розрахунок характеристик телетрафіку")
root.geometry("700x480")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
style.configure("TButton", font=("Segoe UI", 10))

# ====== ЗАГОЛОВОК ======
ttk.Label(root, text="Розрахунок характеристик телетрафіку",
          style="Header.TLabel").pack(pady=10)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# ====== ВХІДНІ ДАНІ ======
input_frame = ttk.LabelFrame(main_frame, text="Вхідні параметри", padding=10)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

labels = [
    "Кількість абонентів",
    "Кількість сеансів зв'язку",
    "Тривалість сеансу (с)",
    "Тривалість робочого дня (хв)",
    "Кількість каналів",
    'Ймовірність "передзвону" (%)'
]

entries = []

for i, text in enumerate(labels):
    ttk.Label(input_frame, text=text).grid(row=i, column=0, sticky="w", pady=4)
    e = ttk.Entry(input_frame, width=20)
    e.grid(row=i, column=1, pady=4)
    entries.append(e)

(ent_users,
 ent_sessions,
 ent_duration,
 ent_day,
 ent_channels,
 ent_recall) = entries

# значення за замовчуванням
defaults = ["1000", "20", "20", "1440", "5", "10"]
for e, v in zip(entries, defaults):
    e.insert(0, v)

# ====== РЕЗУЛЬТАТИ ======
result_frame = ttk.LabelFrame(main_frame, text="Результати розрахунку", padding=10)
result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

def res_row(row, text):
    ttk.Label(result_frame, text=text).grid(row=row, column=0, sticky="w", pady=4)
    lbl = ttk.Label(result_frame, text="—", width=12)
    lbl.grid(row=row, column=1, pady=4)
    return lbl

lbl_A_val  = res_row(0, "Трафік багатоканальної системи A")
lbl_A1_val = res_row(1, "Трафік на канал A₁")
lbl_Pc_val = res_row(2, "Ймовірність затримки Pc")
lbl_Pb_val = res_row(3, "Ймовірність відмови Pb")
lbl_Pa_val = res_row(4, "Ймовірність відмови Pa")

# ====== КНОПКИ ======
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Обчислити", width=20, command=calculate).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Вихід", width=20, command=root.destroy).grid(row=0, column=1, padx=10)

root.mainloop()
