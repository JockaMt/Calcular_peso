"""
Módulo de cálculos de peso de metais
"""
import json
from src.config import CONFIG_PATH, METALS


class Calculator:
    """Classe responsável pelos cálculos de peso de metais"""
    
    def __init__(self):
        self.config_path = CONFIG_PATH
        self._load_config()
    
    def _load_config(self):
        """Carrega a configuração de metais"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = METALS.copy()
            self._save_config()
    
    def _save_config(self):
        """Salva a configuração de metais"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get_density(self, metal_key: str) -> float:
        """Retorna a densidade de um metal"""
        return self.config.get(metal_key, METALS.get(metal_key, 0.0))
    
    def set_density(self, metal_key: str, density: float):
        """Define a densidade de um metal"""
        self.config[metal_key] = density
        self._save_config()
    
    def calculate_weight(self, volume: float, metal_key: str) -> float:
        """Calcula o peso baseado no volume e tipo de metal"""
        try:
            density = self.get_density(metal_key)
            return (float(volume) * density) / 1000
        except (ValueError, TypeError):
            return 0.0
    
    def reset_to_defaults(self):
        """Reseta todos os valores para os padrões"""
        self.config = METALS.copy()
        self._save_config()
    
    def get_all_densities(self) -> dict:
        """Retorna todas as densidades"""
        return self.config.copy()
