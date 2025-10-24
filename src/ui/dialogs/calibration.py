"""
Diálogo de calibração de densidade de metais
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QDoubleSpinBox
)
from src.core.calculator import Calculator


class CalibrationDialog(QDialog):
    """Diálogo para calibração dos valores de densidade de metais"""
    
    METALS = {
        "Ouro 18k": {"key": "Ouro_18k", "default": 15.5},
        "Ouro 14k": {"key": "Ouro_14k", "default": 14.0},
        "Prata 925": {"key": "Prata_925", "default": 10.5}
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = Calculator()
        self.metal_widgets = {}
        self.setup_ui()
        self.load_values()
    
    def setup_ui(self):
        """Configura a interface de usuário"""
        self.setWindowTitle("Configurações de Calibração")
        self.setFixedSize(350, 250)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Cria widgets para cada metal
        for metal_name in self.METALS:
            self.create_metal_widget(main_layout, metal_name)

        # Layout de ações
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        btn_reset = QPushButton("Resetar Valores Padrão")
        btn_reset.clicked.connect(self.reset_to_default)
        action_layout.addWidget(btn_reset)

        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        action_layout.addWidget(btn_close)

        main_layout.addStretch()
        main_layout.addLayout(action_layout)
        self.setLayout(main_layout)

    def create_metal_widget(self, parent_layout, metal_name):
        """Cria os widgets para um metal específico"""
        frame_layout = QHBoxLayout()

        lbl_name = QLabel(f"{metal_name}: ")
        lbl_name.setFixedWidth(100)

        entry_value = QDoubleSpinBox()
        entry_value.setDecimals(3)
        entry_value.setMinimum(0.0)
        entry_value.setMaximum(100.0)
        entry_value.setValue(self.METALS[metal_name]["default"])

        btn_save = QPushButton("Salvar")
        btn_save.setFixedWidth(80)
        btn_save.clicked.connect(lambda: self.save_value(metal_name, entry_value.value()))

        frame_layout.addWidget(lbl_name)
        frame_layout.addWidget(entry_value, 1)
        frame_layout.addWidget(btn_save)

        parent_layout.insertLayout(len(self.metal_widgets), frame_layout)

        self.metal_widgets[metal_name] = {
            "entry_value": entry_value,
            "btn_save": btn_save
        }

    def load_values(self):
        """Carrega os valores atuais da configuração"""
        densities = self.calculator.get_all_densities()

        for metal_name, metal_info in self.METALS.items():
            current_value = densities.get(metal_info["key"], metal_info["default"])
            self.metal_widgets[metal_name]["entry_value"].setValue(float(current_value))

    def save_value(self, metal_name, value):
        """Salva o novo valor na configuração"""
        key = self.METALS[metal_name]["key"]
        self.calculator.set_density(key, value)
        QMessageBox.information(self, "Sucesso", f"Valor de {metal_name} salvo com sucesso!")

    def reset_to_default(self):
        """Reseta todos os valores para os padrões"""
        reply = QMessageBox.question(
            self,
            "Confirmar Reset",
            "Tem certeza que deseja resetar todos os valores para os padrões?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.calculator.reset_to_defaults()
            self.load_values()
            QMessageBox.information(self, "Sucesso", "Valores resetados para os padrões.")
