"""
Módulo para buscar preço do ouro (24k) na inicialização
Usa GoldAPI (https://www.goldapi.io/api/) para obter preço em USD/oz
e ExchangeRate API para conversão para BRL
Cache por 12 horas
"""
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
import os

try:
    import requests
except ImportError:
    requests = None



class GoldPriceCache:
    """Gerencia o cache de preço do ouro"""
    
    # Colocar cache por usuário em %LOCALAPPDATA%/GoldCalculator/.gold_price.json
    try:
        _local_appdata = Path(os.getenv('LOCALAPPDATA') or Path.home())
    except Exception:
        _local_appdata = Path.home()
    CACHE_DIR = _local_appdata / "GoldCalculator"
    CACHE_FILE = CACHE_DIR / ".gold_price.json"
    CACHE_DURATION = timedelta(hours=12)  # Cache válido por 12 horas
    # Chave GoldAPI hardcoded (NÃO expor publicamente)
    GOLDAPI_KEY = "SUA_CHAVE_AQUI"  # Substitua por sua chave real
    OZ_TO_GRAMS = 31.1034768  # 1 troy ounce = 31.1034768 gramas
    
    def __init__(self):
        self.price_brl = None
        self.price_usd_oz = None
        self.fetched_at = None
        self.source = None
        self.api_offline = False
        
    def fetch_price(self) -> float:
        """
        Busca o preço do ouro na inicialização
        Estratégia: 
        1. Verificar cache (se válido e < 12h, usar)
        2. Tentar GoldAPI (se cache expirou)
        3. Usar cache expirado com aviso "- Api offline -"
        4. Vazio
        """
        # Primeiro, tenta carregar do cache
        cache_valid = self._load_from_cache()
        
        # Se cache é válido (menos de 12h), retorna
        if cache_valid and self._is_cache_fresh():
            return self.price_brl
        
        # Se cache expirou, tenta buscar da API
        if self._fetch_from_goldapi():
            return self.price_brl
        
        # Se API falhar mas tem cache expirado, usa com aviso
        if cache_valid and self.price_brl:
            self.api_offline = True
            return self.price_brl
        
        # Se não tem nada, retorna vazio
        self.price_brl = None
        self.api_offline = False
        return self.price_brl
    
    def _is_cache_fresh(self) -> bool:
        """Verifica se o cache ainda é válido (menos de 12h)"""
        if not self.fetched_at:
            return False
        
        try:
            fetched = datetime.fromisoformat(self.fetched_at) if isinstance(self.fetched_at, str) else self.fetched_at
            elapsed = datetime.now() - fetched
            return elapsed < self.CACHE_DURATION
        except Exception:
            return False
    
    def _fetch_from_goldapi(self) -> bool:
        """
        Busca preço do ouro em USD/oz na GoldAPI
        Depois converte para BRL usando ExchangeRate API
        """
        if requests is None or not self.GOLDAPI_KEY:
            return False
        
        try:
            success = [False]
            
            def fetch():
                try:
                    # 1. Buscar preço do ouro em USD/oz
                    response = requests.get(
                        "https://www.goldapi.io/api/XAU/USD",
                        headers={"x-access-token": self.GOLDAPI_KEY},
                        timeout=3
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        price_usd_oz = data.get('price')
                        
                        if price_usd_oz and float(price_usd_oz) > 0:
                            self.price_usd_oz = float(price_usd_oz)
                            
                            # 2. Buscar taxa USD -> BRL
                            rate_response = requests.get(
                                "https://api.exchangerate-api.com/v4/latest/USD",
                                timeout=3,
                                headers={'User-Agent': 'Mozilla/5.0'}
                            )
                            
                            if rate_response.status_code == 200:
                                rate_data = rate_response.json()
                                taxa_brl = rate_data.get('rates', {}).get('BRL')
                                
                                if taxa_brl and taxa_brl > 0:
                                    # 3. Converter: (USD/oz) * taxa_BRL / gramas_por_oz
                                    price_brl_oz = self.price_usd_oz * taxa_brl
                                    self.price_brl = price_brl_oz / self.OZ_TO_GRAMS
                                    self.fetched_at = datetime.now()
                                    self.source = "GoldAPI"
                                    self.api_offline = False
                                    self._save_to_cache()
                                    success[0] = True
                                    return
                except Exception:
                    pass
            
            thread = threading.Thread(target=fetch, daemon=True)
            thread.start()
            thread.join(timeout=4)
            
            return success[0]
            
        except Exception:
            return False
        """
        Busca preço do ouro em USD/oz na GoldAPI
        Depois converte para BRL usando ExchangeRate API
        """
        if requests is None or not self.GOLDAPI_KEY:
            return False
        
        try:
            success = [False]
            
            def fetch():
                try:
                    # 1. Buscar preço do ouro em USD/oz
                    response = requests.get(
                        "https://www.goldapi.io/api/XAU/USD",
                        headers={"x-access-token": self.GOLDAPI_KEY},
                        timeout=3
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        price_usd_oz = data.get('price')
                        
                        if price_usd_oz and float(price_usd_oz) > 0:
                            self.price_usd_oz = float(price_usd_oz)
                            
                            # 2. Buscar taxa USD -> BRL
                            rate_response = requests.get(
                                "https://api.exchangerate-api.com/v4/latest/USD",
                                timeout=3,
                                headers={'User-Agent': 'Mozilla/5.0'}
                            )
                            
                            if rate_response.status_code == 200:
                                rate_data = rate_response.json()
                                taxa_brl = rate_data.get('rates', {}).get('BRL')
                                
                                if taxa_brl and taxa_brl > 0:
                                    # 3. Converter: (USD/oz) * taxa_BRL / gramas_por_oz
                                    price_brl_oz = self.price_usd_oz * taxa_brl
                                    self.price_brl = price_brl_oz / self.OZ_TO_GRAMS
                                    self.fetched_at = datetime.now()
                                    self.source = "GoldAPI"
                                    self._save_to_cache()
                                    success[0] = True
                                    return
                except Exception:
                    pass
            
            thread = threading.Thread(target=fetch, daemon=True)
            thread.start()
            thread.join(timeout=4)
            
            return success[0]
            
        except Exception:
            return False
    
    def _load_from_cache(self) -> bool:
        """Carrega preço do cache local"""
        try:
            if not self.CACHE_FILE.parent.exists():
                # Pasta de cache não existe
                return False
            if self.CACHE_FILE.exists():
                with open(self.CACHE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    price = data.get('price_brl')
                    if price and float(price) > 0:
                        self.price_brl = float(price)
                        self.fetched_at = data.get('fetched_at')
                        self.source = "cache"
                        return True
        except Exception:
            pass
        return False
    
    def _save_to_cache(self):
        """Salva preço no cache local"""
        try:
            # Garante que o diretório exista e é gravável pelo usuário
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'price_brl': self.price_brl,
                    'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None,
                    'source': self.source
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def get_price_text(self) -> str:
        """Retorna o preço formatado para exibição"""
        if self.price_brl is None or self.price_brl <= 0:
            return ""  # Vazio se não conseguiu

        return "- Api offline -" if self.api_offline else f"Ouro 24k: R$ {self.price_brl:.2f}/g"
