import tkinter as tk
from tkinter import ttk

import calculo


class Calibration(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.lista = []

        self.get_valores()

        self.item_1()
        self.item_2()
        self.item_3()
        self.item_4()

    def get_valores(self):
        self.lista = []
        for i in calculo.get_data():
            self.lista.append(calculo.get_data()[i])

    def item_1(self):
        self.frame1 = tk.Frame(self.parent)
        self.label1 = tk.Label(self.frame1, text="Ouro 18k: ")
        self.label1.pack(side=tk.LEFT)
        self.label2 = tk.Label(self.frame1, text=self.lista[0])
        self.label2.pack(side=tk.LEFT, expand=True)
        self.entry1 = tk.Entry(self.frame1)
        self.entry1.pack_forget()
        self.but1 = ttk.Button(self.frame1, text="Editar", command=lambda: self.edit(0))
        self.but1.pack(side=tk.LEFT)
        self.frame1.pack(fill=tk.X, pady=(10, 5), padx=10)

    def item_2(self):
        self.frame2 = tk.Frame(self.parent)
        self.label3 = tk.Label(self.frame2, text="Ouro 14k: ")
        self.label3.pack(side=tk.LEFT)
        self.label4 = tk.Label(self.frame2, text=self.lista[1])
        self.label4.pack(side=tk.LEFT, expand=True)
        self.entry2 = tk.Entry(self.frame2)
        self.entry2.pack_forget()
        self.but2 = ttk.Button(self.frame2, text="Editar", command=lambda: self.edit(1))
        self.but2.pack(side=tk.LEFT)
        self.frame2.pack(fill=tk.X, padx=10)

    def item_3(self):
        self.frame3 = tk.Frame(self.parent)
        self.label5 = tk.Label(self.frame3, text="Prata 925: ")
        self.label5.pack(side=tk.LEFT)
        self.label6 = tk.Label(self.frame3, text=self.lista[2])
        self.label6.pack(side=tk.LEFT, expand=True)
        self.entry3 = tk.Entry(self.frame3)
        self.entry3.pack_forget()
        self.but3 = ttk.Button(self.frame3, text="Editar", command=lambda: self.edit(2))
        self.but3.pack(side=tk.LEFT)
        self.frame3.pack(fill=tk.X, pady=5, padx=10)

    def item_4(self):
        self.frame4 = tk.Frame(self.parent)
        self.but4 = ttk.Button(self.frame4, text="Resetar", command=self.reset)
        self.but4.pack(side=tk.LEFT, expand=True)
        self.frame4.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def edit(self, item):
        match item:
            case 0:
                self.label2.pack_forget()
                self.but1.pack_forget()
                self.entry1.pack(side=tk.LEFT, expand=True)
                self.but1.config(text='Salvar', command=lambda : self.save("Ouro_18k", float(str(self.entry1.get()).replace(",", "."))) if self.entry1.get() != "" else self.save("Ouro_18k", self.lista[0]))
                self.but1.pack(side=tk.LEFT)
            case 1:
                self.label4.pack_forget()
                self.but2.pack_forget()
                self.entry2.pack(side=tk.LEFT, expand=True)
                self.but2.pack(side=tk.LEFT)
                self.but2.config(text='Salvar', command=lambda : self.save("Ouro_14k", float(str(self.entry2.get()).replace(",", "."))) if self.entry2.get() != "" else self.save("Ouro_14k", self.lista[1]))
            case 2:
                self.label6.pack_forget()
                self.but3.pack_forget()
                self.entry3.pack(side=tk.LEFT, expand=True)
                self.but3.pack(side=tk.LEFT)
                self.but3.config(text='Salvar', command=lambda : self.save("Prata_925", float(str(self.entry3.get()).replace(",", "."))) if self.entry3.get() != "" else self.save("Prata_925", self.lista[2]))


    def save(self, key, new_data):
        calculo.salvar(key, new_data)
        self.get_valores()
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.item_1()
        self.item_2()
        self.item_3()
        self.item_4()

    def reset(self):
        calculo.resetar()
        self.save("Ouro_18k", 15.5)