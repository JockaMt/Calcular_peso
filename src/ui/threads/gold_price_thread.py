"""
Thread para atualização periódica de cotação de ouro
"""
from PySide6.QtCore import QThread, Signal
from src.core.gold_price import GoldPriceManager


class GoldPriceThread(QThread):
    """Thread para buscar a cotação do ouro periodicamente"""
    
    price_updated = Signal(str)
    
    def __init__(self, update_interval: int = 60):
        super().__init__()
        self.is_running = True
        self.daemon = True
        self.update_interval = update_interval
        self.gold_manager = GoldPriceManager()
    
    def run(self):
        """Executa a thread para buscar a cotação"""
        import time
        
        while self.is_running:
            try:
                price_data = self.gold_manager.get_price_brl()
                if price_data:
                    self._emit_price(price_data)
                else:
                    self.price_updated.emit("Cotação do Ouro: Indisponível")
            except Exception as e:
                self.price_updated.emit("Cotação do Ouro: Indisponível")
            
            # Aguarda em blocos pequenos para permitir interrupção
            for _ in range(self.update_interval):
                if not self.is_running:
                    return
                time.sleep(1)
    
    def _emit_price(self, price_data: dict):
        """Emite o sinal com as informações de preço formatadas"""
        price = price_data['price_brl']
        is_default = price_data.get('is_default', False)
        from_cache = price_data.get('from_cache', False)
        
        suffix = ""
        if is_default:
            suffix = " (Padrão)"
        elif from_cache:
            suffix = " (Cache)"
        
        status_text = f"Cotação do Ouro: R$ {price:.2f}/g (BRL) {suffix}"
        self.price_updated.emit(status_text)
    
    def stop(self):
        """Para a thread"""
        self.is_running = False
