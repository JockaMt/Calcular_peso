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
GOLD_PRICE_CACHE_PATH = BASE_PATH / ".gold_price_cache.json"

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

# ==================== COTAÇÃO DE OURO ====================
DEFAULT_GOLD_PRICE_USD = 65.50  # USD por grama
DEFAULT_GOLD_PRICE_BRL = 352.50  # BRL por grama

GOLD_UPDATE_INTERVAL = 60  # segundos
GOLD_THREAD_TIMEOUT = 5000  # millisegundos (5 segundos)

# ==================== INTERFACE ====================
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

# ==================== API ====================
EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/USD"
EXCHANGE_RATE_TIMEOUT = 5  # segundos

# ==================== LOGGING ====================
DEBUG = False
