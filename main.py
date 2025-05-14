import json
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import calculo
from menu.script import Calibration

def get_base_path():
    """Retorna o caminho base dependendo se está executando como script ou executável"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        return Path(sys.executable).parent
    else:
        # Se estiver rodando como script
        return Path(__file__).parent

BASE_PATH = get_base_path()
CONFIG_PATH = BASE_PATH / "config.json"

class MetalWeightCalculator:
    def __init__(self, root):
        self.root = root
        self.choice = 0  # 0: Ouro 18k, 1: Ouro 14k, 2: Prata 925
        self.setup_ui()
        self.setup_menu()
        self.ensure_config_file()

    def ensure_config_file(self):
        """Cria o arquivo de configuração com valores padrão se não existir"""
        if not CONFIG_PATH.exists():
            default_config = {
                "Ouro_18k": 15.5,
                "Ouro_14k": 14.0,
                "Prata_925": 10.5
            }
            with open(CONFIG_PATH, 'w') as f:
                json.dump(default_config, f)
        
    def setup_ui(self):
        """Configura a interface gráfica principal"""
        self.root.title('Calculadora de Pesos de Metais')
        self.root.resizable(False, False)
        self.center_window(400, 200)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Frame de entrada
        self.setup_input_frame(main_frame)
        
        # Frame de botões de opção
        self.setup_options_frame(main_frame)
        
        # Frame de resultado
        self.setup_result_frame(main_frame)
        
    def setup_input_frame(self, parent):
        """Configura o frame de entrada de dados"""
        input_frame = ttk.Frame(parent)
        
        lbl_volume = ttk.Label(input_frame, text='Volume:')
        lbl_volume.pack(side=tk.LEFT)
        
        self.entry_volume = ttk.Entry(input_frame)
        self.entry_volume.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        self.entry_volume.bind('<Return>', lambda e: self.update_result())  # Enter para calcular
        
        btn_calculate = ttk.Button(input_frame, text='Calcular', command=self.update_result)
        btn_calculate.pack(side=tk.LEFT)
        
        input_frame.pack(fill='x', pady=(0, 10))
        
    def setup_options_frame(self, parent):
        """Configura os botões de seleção de metal"""
        options_frame = ttk.Frame(parent)
        
        self.metal_buttons = []
        metals = [
            ("Ouro 18k", 0),
            ("Ouro 14k", 1),
            ("Prata 925", 2)
        ]
        
        for text, value in metals:
            btn = ttk.Button(
                options_frame, 
                text=text,
                command=lambda v=value: self.change_metal(v)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.metal_buttons.append(btn)
            
        # Desativa o botão padrão (Ouro 18k)
        self.metal_buttons[self.choice].config(state=tk.DISABLED)
        
        options_frame.pack(pady=5)
        
    def setup_result_frame(self, parent):
        """Configura a área de exibição do resultado"""
        result_frame = ttk.Frame(parent)
        
        self.lbl_result = ttk.Label(
            result_frame, 
            text='Peso: 0.000g', 
            font=('TkDefaultFont', 10, 'bold')
        )
        self.lbl_result.pack(expand=True)
        
        result_frame.pack(fill='x', pady=10)
        
    def setup_menu(self):
        """Configura o menu superior"""
        menubar = tk.Menu(self.root)
        
        # Menu Configurações
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(
            label='Calibrar cálculo...', 
            command=self.open_settings
        )
        settings_menu.add_separator()
        settings_menu.add_command(
            label='Sair', 
            command=self.on_closing
        )
        
        menubar.add_cascade(label='Configurações', menu=settings_menu)
        self.root.config(menu=menubar)
        
    def center_window(self, width, height):
        """Centraliza a janela na tela"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def change_metal(self, option):
        """Altera o tipo de metal selecionado"""
        self.choice = option
        for i, btn in enumerate(self.metal_buttons):
            btn.config(state=tk.DISABLED if i == option else tk.NORMAL)
        self.update_result()
        
    def update_result(self):
        """Atualiza o resultado do cálculo"""
        try:
            volume = self.entry_volume.get().replace(",", ".")
            if not volume:  # Se o campo estiver vazio
                self.lbl_result.config(text='Peso: 0.000g')
                return
                
            weight = calculo.calculate(float(volume), self.choice)
            self.lbl_result.config(text=f'Peso: {weight:.3f}g')
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
            self.entry_volume.focus_set()
            
    def open_settings(self):
        """Abre a janela de configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurações")
        settings_window.geometry("300x200")
        settings_window.grab_set()
        
        calibration = Calibration(settings_window)
        calibration.pack(fill=tk.BOTH, expand=True)
        
    def on_closing(self):
        """Lida com o fechamento da aplicação"""
        if messagebox.askokcancel("Sair", "Deseja mesmo sair do programa?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = MetalWeightCalculator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()