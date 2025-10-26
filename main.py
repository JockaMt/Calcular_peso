"""
Calculadora de Pesos de Metais - Aplicação Principal
Versão PySide6 com Arquitetura Modular
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import os
import hashlib
import subprocess

from src.ui.main_window import MainWindow


def get_machine_id():
    try:
        result = subprocess.check_output('wmic diskdrive get serialnumber', shell=True)
        serial = result.decode(errors='ignore').split('\n')[1].strip()
        return hashlib.sha256(serial.encode()).hexdigest()
    except Exception:
        return None


def check_license():
    license_file = os.path.expanduser('~/.goldcalc.lic')
    machine_id = get_machine_id()
    if not machine_id:
        sys.exit("Erro ao obter ID da máquina.")
    if not os.path.exists(license_file):
        with open(license_file, 'w') as f:
            f.write(machine_id)
    else:
        with open(license_file) as f:
            saved_id = f.read().strip()
        if saved_id != machine_id:
            sys.exit("Licença inválida para esta máquina.")


def main():
    """Função principal da aplicação"""
    # Configurar DPI antes de criar a aplicação
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    check_license()
    main()
