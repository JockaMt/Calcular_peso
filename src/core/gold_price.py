"""
Módulo para gerenciar cotação de ouro
"""
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from src.config import (
    DEFAULT_GOLD_PRICE_USD,
    DEFAULT_GOLD_PRICE_BRL,
    GOLD_PRICE_CACHE_PATH,
    EXCHANGE_RATE_API_URL,
    EXCHANGE_RATE_TIMEOUT
)


class GoldPriceManager:
    """Classe responsável por gerenciar cotações de ouro"""
    
    def __init__(self):
        self.cache_path = GOLD_PRICE_CACHE_PATH
        self.exchange_api_url = EXCHANGE_RATE_API_URL
        self.timeout = EXCHANGE_RATE_TIMEOUT
        self.melhorcambio_url = "https://www.melhorcambio.com/ouro-hoje"
    
    def _load_cache(self) -> dict:
        """Carrega a cotação em cache se existir"""
        try:
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def _save_cache(self, price_data: dict):
        """Salva a cotação em cache"""
        try:
            with open(self.cache_path, 'w') as f:
                json.dump(price_data, f, indent=4)
        except Exception:
            pass
    
    def _fetch_gold_price_from_melhorcambio(self) -> float:
        """
        Busca a cotação de ouro 24K diretamente do site MelhorCâmbio
        usando web scraping silencioso (sem alertar o usuário de falhas)
        """
        try:
            # Simula um navegador real para evitar bloqueios
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(
                self.melhorcambio_url,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Procura pelo valor em R$ 713,38 na página
                # Busca por padrões comuns de preço
                price_text = None
                
                # Estratégia 1: Procura por "R$ XXX,XX" ou "R$XXX,XX"
                for element in soup.find_all(['span', 'div', 'p']):
                    text = element.get_text(strip=True)
                    if 'R$' in text and ',' in text and len(text) < 30:
                        # Tenta extrair o número
                        try:
                            # Remove "R$" e espaços
                            price_str = text.replace('R$', '').strip()
                            # Converte vírgula em ponto para float
                            price_float = float(price_str.replace(',', '.'))
                            # Valida se está em range razoável (200-1000 BRL/g)
                            if 200 < price_float < 1000:
                                price_text = price_float
                                break
                        except (ValueError, AttributeError):
                            continue
                
                # Estratégia 2: Procura por inputs ou valores em atributos
                if not price_text:
                    for element in soup.find_all('input'):
                        value = element.get('value', '')
                        if 'R$' in str(value) or (',' in str(value) and '.' not in str(value)):
                            try:
                                price_str = str(value).replace('R$', '').strip()
                                price_float = float(price_str.replace(',', '.'))
                                if 200 < price_float < 1000:
                                    price_text = price_float
                                    break
                            except ValueError:
                                continue
                
                if price_text:
                    return price_text
                    
        except (requests.RequestException, Exception):
            # Silencioso - falhas são tratadas com cache/padrão
            pass
        
        return None
        """Busca a taxa de câmbio USD/BRL atual"""
        try:
            response = requests.get(
                self.exchange_api_url,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rates', {}).get('BRL')
                if rate:
                    return float(rate)
        except (requests.RequestException, ValueError, KeyError):
            pass
        
        return None
    
    def get_price_brl(self) -> dict:
        """
        Busca a cotação do ouro em BRL por grama
        Prioridade: Web Scraping MelhorCâmbio → Taxa USD/BRL → Cache → Padrão
        """
        
        # 1. Tenta web scraping direto do MelhorCâmbio (mais preciso)
        price_from_scraping = self._fetch_gold_price_from_melhorcambio()
        if price_from_scraping:
            price_data = {
                'price_brl': price_from_scraping,
                'currency': 'BRL',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'from_cache': False,
                'is_default': False,
                'source': 'melhorcambio'
            }
            self._save_cache(price_data)
            return price_data
        
        # 2. Se falhar, tenta buscar taxa de câmbio atualizada
        usd_to_brl = self.get_usd_to_brl_rate()
        if usd_to_brl:
            price_per_gram_brl = DEFAULT_GOLD_PRICE_USD * usd_to_brl
            
            price_data = {
                'price_brl': price_per_gram_brl,
                'price_usd': DEFAULT_GOLD_PRICE_USD,
                'currency': 'BRL',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'from_cache': False,
                'is_default': False,
                'source': 'exchangerate-api'
            }
            self._save_cache(price_data)
            return price_data
        
        # 3. Se falhar, tenta usar cache
        cached = self._load_cache()
        if cached and 'price_brl' in cached:
            cached['from_cache'] = True
            cached['is_default'] = False
            cached['timestamp'] = datetime.now().strftime('%H:%M:%S')
            return cached
        
        # 4. Se não houver cache, usa valor padrão
        return {
            'price_brl': DEFAULT_GOLD_PRICE_BRL,
            'price_usd': DEFAULT_GOLD_PRICE_USD,
            'currency': 'BRL',
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'from_cache': False,
            'is_default': True,
            'source': 'default'
        }
    
    def get_price_usd(self) -> dict:
        """Busca a cotação do ouro em USD por grama"""
        
        # Tenta usar cache primeiro
        cached = self._load_cache()
        if cached and 'price_usd' in cached:
            cached['from_cache'] = True
            cached['is_default'] = False
            cached['timestamp'] = datetime.now().strftime('%H:%M:%S')
            return cached
        
        # Usa valor padrão
        return {
            'price_usd': DEFAULT_GOLD_PRICE_USD,
            'currency': 'USD',
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'from_cache': False,
            'is_default': True
        }
