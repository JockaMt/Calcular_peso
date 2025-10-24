"""
Utilitários para manipulação de caminhos
"""
from pathlib import Path
import sys

def get_base_path():
    """Retorna o caminho base dependendo se está executando como script ou executável"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        return Path(sys.executable).parent
    else:
        # Se estiver rodando como script
        return Path(__file__).parent.parent.parent
