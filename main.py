"""
Calculadora de Pesos de Metais - Aplicação Principal
Versão PySide6 com Arquitetura Modular
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.ui.main_window import MainWindow


def main():
    """Função principal da aplicação"""
    # Configurar DPI antes de criar a aplicação
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
