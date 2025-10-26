"""
Arquivo de configurações centralizadas da aplicação
"""
from pathlib import Path
import sys

# ==================== CAMINHOS ====================
def get_base_path():
    """Retorna o caminho base dependendo se está executando como script ou executável"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent.parent

BASE_PATH = get_base_path()
CONFIG_PATH = BASE_PATH / "config.json"

# ==================== METAIS ====================
METALS = {
    "Ouro_18k": 15.5,
    "Ouro_14k": 14.0,
    "Prata_925": 10.5
}

METAL_LABELS = {
    0: "Ouro 18k",
    1: "Ouro 14k",
    2: "Prata 925"
}

# ==================== INTERFACE ====================
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

# ==================== LOGGING ====================
DEBUG = False
