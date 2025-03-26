import os
from tkinter import *
from tkinter import ttk, messagebox

SETTINGS_FILE = "settings.py"


def save_settings(params):
    """Сохраняет параметры в файл settings.py"""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            f.write(f"t0 = {float(params['t0'])}\n")
            f.write(f"n = {int(params['n'])}\n")
            f.write(f"t = t0 / (n - 1)\n")
            f.write(f"g = {float(params['g'])}\n")
            f.write(f"m = {float(params['m'])}\n")
            f.write(f"vx = {float(params['vx'])}\n")
            f.write(f"vy = {float(params['vy'])}\n")
            f.write(f"x = {float(params['x'])}\n")
            f.write(f"y = {float(params['y'])}\n")
            f.write(f"size = {float(params['size'])}\n\n")
            f.write("# Инициализация массивов\n")
            f.write("keys = 0\n")
            f.write("vu = 0\n")
            f.write(f"xr = [{float(params['x'])}]\n")
            f.write(f"yr = [{float(params['y'])}]\n")
            f.write(f"vxr = [{float(params['vx'])}]\n")
            f.write(f"vyr = [{float(params['vy'])}]\n")
        return True
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить параметры:\n{str(e)}")
        return False


def run_calculation():
    try:
        # Получаем значения из полей ввода
        params = {
            't0': entry_t0.get(),
            'n': entry_n.get(),
            'g': entry_g.get(),
            'm': entry_m.get(),
            'vx': entry_vx.get(),
            'vy': entry_vy.get(),
            'x': entry_x.get(),
            'y': entry_y.get(),
            'size': entry_size.get()
        }

        # Проверка заполненности полей
        for key, value in params.items():
            if not value.strip():
                messagebox.showerror("Ошибка", f"Поле '{key}' не заполнено!")
                return

        # Преобразование и проверка значений
        try:
            params = {k: float(v) if k not in ['n'] else int(v) for k, v in params.items()}
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения!")
            return

        if params['n'] <= 1:
            messagebox.showerror("Ошибка", "Количество шагов (n) должно быть больше 1")
            return

        # Сохранение параметров
        if save_settings(params):
            t = params['t0'] / (params['n'] - 1)
            messagebox.showinfo("Gravity Sim",
                                f"Параметры успешно сохранены в {SETTINGS_FILE}\n"
                                f"Рассчитанный шаг времени: t = {t:.2e}")
            root.destroy()  # Закрываем окно после успешного сохранения

    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла ошибка:\n{str(e)}")


def create_dark_theme():
    style = ttk.Style()
    style.theme_use('alt')

    # Цвета темы
    bg_color = '#333333'
    fg_color = '#ffffff'
    entry_bg = '#555555'
    accent_color = '#0078d7'

    # Настройка стилей
    style.configure('.', background=bg_color, foreground=fg_color)
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color)
    style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color, insertcolor=fg_color)
    style.configure('TButton', background='#555555', foreground=fg_color)
    style.configure('Accent.TButton', background=accent_color, foreground=fg_color)

    style.map('TButton',
              background=[('active', '#666666')],
              foreground=[('active', fg_color)])
    style.map('Accent.TButton',
              background=[('active', '#0066b4')],
              foreground=[('active', fg_color)])


# Создание главного окна
dir = os.path.abspath(os.curdir)

root = Tk()
root.title("Gravity Sim")
root.iconbitmap(dir + "\\icon.ico")
root.geometry("600x600")

# Применение темной темы
create_dark_theme()

# Основной контейнер
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=BOTH, expand=True)

# Фрейм параметров
params_frame = ttk.LabelFrame(main_frame, text="Параметры моделирования", padding=15)
params_frame.pack(fill=BOTH, expand=True)

# Дефолтные значения
defaults = {
    "t0": "50000000000",
    "n": "100000",
    "g": "6.67e-11",
    "m": "1.9891e30",
    "vx": "0",
    "vy": "13070",
    "x": "740573600000",
    "y": "740573600000",
    "size": "8000000000"
}

# Создание полей ввода
entries = {}
for row, (label, key) in enumerate([
    ("Общее время моделирования, t0:", "t0"),
    ("Количество шагов, n:", "n"),
    ("Гравитационная постоянная, g:", "g"),
    ("Масса центрального тела, m:", "m"),
    ("Начальная скорость по X, vx:", "vx"),
    ("Начальная скорость по Y, vy:", "vy"),
    ("Начальная координата X, x:", "x"),
    ("Начальная координата Y, y:", "y"),
    ("Масштаб отображения, size:", "size")
]):
    frame = ttk.Frame(params_frame)
    frame.grid(row=row, column=0, sticky="ew", pady=5)

    ttk.Label(frame, text=label, width=30).pack(side=LEFT, padx=5)
    entry = ttk.Entry(frame)
    entry.pack(side=RIGHT, expand=True, fill=X, padx=5)
    entry.insert(0, defaults[key])
    entries[key] = entry

# Привязка переменных
entry_t0 = entries["t0"]
entry_n = entries["n"]
entry_g = entries["g"]
entry_m = entries["m"]
entry_vx = entries["vx"]
entry_vy = entries["vy"]
entry_x = entries["x"]
entry_y = entries["y"]
entry_size = entries["size"]

# Кнопка сохранения
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=X, pady=15)

ttk.Button(
    button_frame,
    text="Сохранить параметры",  # Изменили текст кнопки
    command=run_calculation,
    style='Accent.TButton'
).pack(side=RIGHT)

# Запуск приложения
root.mainloop()