import tkinter as tk
from tkinter import ttk
import calculo
from menu.calibration import Calibration

choice = 0

def update_label():
    global choice
    try:
        volume = entry.get().replace(",", ".")
        valor = calculo.calculate(volume, choice)
        label['text'] = f'Peso: {valor:.3f}g'
    except ValueError:
        return None

def change_choice(opt):
    buttons = [au18, au16, prata750]
    global choice
    match opt:
        case 0:
            choice = 0
        case 1:
            choice = 1
        case 2:
            choice = 2
        case 3:
            choice = 3

    for i, j in enumerate(buttons):
        if i != choice:
            j.config(state=tk.NORMAL)
        else:
            j.config(state=tk.DISABLED)

app = tk.Tk()


def get_wm_info(height_size, wight_size, h, w):
    x = int((wight_size / 2) - (w / 2))
    y = int((height_size / 2) - (h / 2))
    return f'{w}x{h}+{x}+{y}'

def settings(root):
    setting = tk.Toplevel(root)
    setting.geometry(get_wm_info(setting.winfo_screenheight(), setting.winfo_screenwidth(), 200, 300))
    setting.grab_set()
    calibration = Calibration(setting)
    calibration.pack(fill=tk.BOTH, expand=True)

# set the dimensions of the screen
# and where it is placed


ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight()
app.geometry(get_wm_info(hs, ws, 200, 400))

app.resizable(False, False)
app.title('Calcular pesos')
frame = ttk.Frame(app)

entry_frame = ttk.Frame(frame)
text = ttk.Label(entry_frame, text='Volume:')
text.pack(side=tk.LEFT)
entry = ttk.Entry(entry_frame)
entry.pack(padx=20, ipady=5, expand=True, fill='x', side=tk.LEFT)
button = ttk.Button(entry_frame, text='Calcular', command=update_label)
button.pack(side=tk.LEFT, expand=False, fill='y')
entry.focus_set()
entry_frame.pack(pady=5, padx=10, expand=False, fill='x')

separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X)

options_buttons_frame = ttk.Frame(frame)

au18 = ttk.Button(options_buttons_frame, text="Ouro 18k", state=tk.DISABLED, command=lambda: change_choice(0))
au18.pack(side=tk.LEFT)

au16 = ttk.Button(options_buttons_frame, text="Ouro 14k", command=lambda: change_choice(1))
au16.pack(side=tk.LEFT)

prata750 = ttk.Button(options_buttons_frame, text="Prata 925", command=lambda: change_choice(2))
prata750.pack(side=tk.LEFT)
options_buttons_frame.pack(padx=5, pady=5)

separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X)

label_frame = ttk.Frame(frame)

label = ttk.Label(label_frame, text='')
label.pack()

label_frame.pack(expand=True, fill='x')

frame.pack(expand=True, fill='both')

menu = tk.Menu(app)
settings_menu = tk.Menu(menu, tearoff=0)
settings_menu.add_command(label='Calibrar cálculo...', command=lambda: settings(app))
menu.add_cascade(label='Settings', menu=settings_menu)

app.config(menu=menu)
app.mainloop()