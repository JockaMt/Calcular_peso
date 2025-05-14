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
        return Path(__file__).parent

BASE_PATH = get_base_path()
CONFIG_PATH = BASE_PATH / "config.json"

def get_data():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Retorna valores padrão se o arquivo não existir ou for inválido
        return {
            "Ouro_18k": 15.5,
            "Ouro_14k": 14.0,
            "Prata_925": 10.5
        }

def salvar(key, value):
    data = get_data()
    data[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def resetar():
    default_values = {
        "Ouro_18k": 15.5,
        "Ouro_14k": 14.0,
        "Prata_925": 10.5
    }
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_values, f, indent=4)

def calculate(volume, choice):
    data = get_data()
    metals = ["Ouro_18k", "Ouro_14k", "Prata_925"]
    if 0 <= choice < len(metals):
        return (float(volume) * data[metals[choice]]) / 1000
    return 0.0