import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import sys
import os

def get_base_path():
    """Retorna o caminho base dependendo se está executando como script ou executável"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        return Path(sys.executable).parent
    else:
        # Se estiver rodando como script
        return Path(__file__).parent.parent

BASE_PATH = get_base_path()
CONFIG_PATH = BASE_PATH / "config.json"

class Calibration(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.metal_data = {
            "Ouro 18k": {"key": "Ouro_18k", "default": 15.5},
            "Ouro 14k": {"key": "Ouro_14k", "default": 14.0},
            "Prata 925": {"key": "Prata_925", "default": 10.5}
        }
        
        self.setup_ui()
        self.load_values()
        
    def setup_ui(self):
        """Configura a interface de usuário"""
        self.parent.title("Configurações de Calibração")
        
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.metal_widgets = {}
        for metal_name in self.metal_data:
            self.create_metal_widget(main_frame, metal_name)
        
        self.setup_action_buttons(main_frame)
    
    def create_metal_widget(self, parent, metal_name):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        lbl_name = tk.Label(frame, text=f"{metal_name}: ", width=10, anchor='w')
        lbl_name.pack(side=tk.LEFT)
        
        lbl_value = tk.Label(frame, text="", width=10)
        lbl_value.pack(side=tk.LEFT, padx=5)
        
        entry_value = tk.Entry(frame, width=10)
        
        btn_edit = ttk.Button(frame, text="Editar", width=8,
                            command=lambda m=metal_name: self.toggle_edit_mode(m))
        btn_edit.pack(side=tk.RIGHT)
        
        self.metal_widgets[metal_name] = {
            "frame": frame,
            "lbl_value": lbl_value,
            "entry_value": entry_value,
            "btn_edit": btn_edit,
            "edit_mode": False
        }
    
    def setup_action_buttons(self, parent):
        action_frame = tk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(15, 5))
        
        btn_reset = ttk.Button(
            action_frame, 
            text="Resetar Valores Padrão",
            command=self.reset_to_default
        )
        btn_reset.pack(side=tk.LEFT, expand=True)
        
    def load_values(self):
        """Carrega os valores atuais da configuração"""
        try:
            with open(CONFIG_PATH, 'r') as f:
                config_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config_data = {info["key"]: info["default"] for _, info in self.metal_data.items()}
        
        for metal_name, metal_info in self.metal_data.items():
            current_value = config_data.get(metal_info["key"], metal_info["default"])
            self.metal_widgets[metal_name]["lbl_value"].config(text=f"{current_value:.3f}")
            self.metal_widgets[metal_name]["entry_value"].delete(0, tk.END)
            self.metal_widgets[metal_name]["entry_value"].insert(0, str(current_value))
    
    def toggle_edit_mode(self, metal_name):
        widgets = self.metal_widgets[metal_name]
        
        if widgets["edit_mode"]:
            try:
                new_value = float(widgets["entry_value"].get().replace(",", "."))
                self.save_value(metal_name, new_value)
                widgets["lbl_value"].config(text=f"{new_value:.3f}")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
                return
            
            widgets["entry_value"].pack_forget()
            widgets["lbl_value"].pack(side=tk.LEFT, padx=5)
            widgets["btn_edit"].config(text="Editar")
            widgets["edit_mode"] = False
        else:
            widgets["lbl_value"].pack_forget()
            widgets["entry_value"].pack(side=tk.LEFT, padx=5)
            widgets["btn_edit"].config(text="Salvar")
            widgets["edit_mode"] = True
            widgets["entry_value"].focus_set()
    
    def save_value(self, metal_name, value):
        """Salva o novo valor na configuração"""
        key = self.metal_data[metal_name]["key"]
        
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        data[key] = value
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    
    def reset_to_default(self):
        """Reseta todos os valores para os padrões"""
        if messagebox.askyesno(
            "Confirmar Reset",
            "Tem certeza que deseja resetar todos os valores para os padrões?"
        ):
            data = {}
            for metal_name, metal_info in self.metal_data.items():
                data[metal_info["key"]] = metal_info["default"]
                self.save_value(metal_name, metal_info["default"])
            
            self.load_values()
            messagebox.showinfo("Sucesso", "Valores resetados para os padrões.")