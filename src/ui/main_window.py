"""
Janela principal da aplicação
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtGui import QFont
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, METAL_LABELS, GOLD_THREAD_TIMEOUT
from src.core.calculator import Calculator
from src.ui.threads.gold_price_thread import GoldPriceThread
from src.ui.dialogs.calibration import CalibrationDialog


class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.choice = 0  # 0: Ouro 18k, 1: Ouro 14k, 2: Prata 925
        self.metal_buttons = []
        self.gold_price_thread = None
        self.calculator = Calculator()
        
        self.setup_ui()
        self.start_gold_price_updater()
    
    def setup_ui(self):
        """Configura a interface gráfica principal"""
        self.setWindowTitle('Calculadora de Pesos de Metais')
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Frame de entrada
        self._setup_input_section(main_layout)
        
        # Frame de botões de metal
        self._setup_metal_buttons_section(main_layout)
        
        # Frame de resultado
        self._setup_result_section(main_layout)

        main_layout.addStretch()
        central_widget.setLayout(main_layout)

        # Configura o menu
        self._setup_menu()
        
        # Configura a barra de status
        self._setup_status_bar()

        # Centraliza a janela
        self._center_window()
    
    def _setup_input_section(self, parent_layout):
        """Configura o frame de entrada de dados"""
        input_layout = QHBoxLayout()
        
        lbl_volume = QLabel('Volume:')
        self.entry_volume = QLineEdit()
        self.entry_volume.returnPressed.connect(self.update_result)
        
        btn_calculate = QPushButton('Calcular')
        btn_calculate.clicked.connect(self.update_result)
        
        input_layout.addWidget(lbl_volume)
        input_layout.addWidget(self.entry_volume, 1)
        input_layout.addWidget(btn_calculate)
        parent_layout.addLayout(input_layout)
    
    def _setup_metal_buttons_section(self, parent_layout):
        """Configura os botões de seleção de metal"""
        options_layout = QHBoxLayout()
        
        metals = [
            ("Ouro 18k", 0),
            ("Ouro 14k", 1),
            ("Prata 925", 2)
        ]

        for text, value in metals:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked=False, v=value: self.change_metal(v))
            btn.setCheckable(True)
            if value == 0:
                btn.setChecked(True)
            options_layout.addWidget(btn)
            self.metal_buttons.append(btn)

        parent_layout.addLayout(options_layout)
    
    def _setup_result_section(self, parent_layout):
        """Configura a área de exibição do resultado"""
        result_layout = QHBoxLayout()
        
        self.lbl_result = QLabel('Peso: 0.000g')
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.lbl_result.setFont(font)
        result_layout.addWidget(self.lbl_result)
        parent_layout.addLayout(result_layout)
    
    def _setup_menu(self):
        """Configura o menu superior"""
        menubar = self.menuBar()
        
        # Menu Configurações
        settings_menu = menubar.addMenu('Configurações')
        
        calibrate_action = settings_menu.addAction('Calibrar cálculo...')
        calibrate_action.triggered.connect(self.open_settings)
        
        settings_menu.addSeparator()
        
        exit_action = settings_menu.addAction('Sair')
        exit_action.triggered.connect(self.on_closing)
    
    def _setup_status_bar(self):
        """Configura a barra de status"""
        self.status_label = QLabel('Cotação do Ouro: Carregando...')
        self.statusBar().addWidget(self.status_label)
    
    def _center_window(self):
        """Centraliza a janela na tela"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        x = (screen_width // 2) - (self.width() // 2)
        y = (screen_height // 2) - (self.height() // 2)

        self.move(x, y)
    
    def start_gold_price_updater(self):
        """Inicia a thread para atualizar a cotação do ouro"""
        self.gold_price_thread = GoldPriceThread()
        self.gold_price_thread.price_updated.connect(self.update_status_bar)
        self.gold_price_thread.start()
        
        # Busca inicial
        self.update_gold_price_immediate()
    
    def update_gold_price_immediate(self):
        """Faz uma busca imediata da cotação"""
        try:
            from src.core.gold_price import GoldPriceManager
            manager = GoldPriceManager()
            price_data = manager.get_price_brl()
            
            if price_data:
                price = price_data['price_brl']
                is_default = price_data.get('is_default', False)
                from_cache = price_data.get('from_cache', False)
                
                suffix = ""
                if is_default:
                    suffix = " (Padrão)"
                elif from_cache:
                    suffix = " (Cache)"
                
                self.status_label.setText(f"Cotação do Ouro: R$ {price:.2f}/g (BRL){suffix}")
            else:
                self.status_label.setText("Cotação do Ouro: Indisponível")
        except Exception:
            self.status_label.setText("Cotação do Ouro: Indisponível")
    
    def update_status_bar(self, status_text):
        """Atualiza o texto da barra de status"""
        self.status_label.setText(status_text)
    
    def change_metal(self, option):
        """Altera o tipo de metal selecionado"""
        self.choice = option
        for i, btn in enumerate(self.metal_buttons):
            btn.setChecked(i == option)
        self.update_result()

    def update_result(self):
        """Atualiza o resultado do cálculo"""
        try:
            volume = self.entry_volume.text().replace(",", ".")
            if not volume:  # Se o campo estiver vazio
                self.lbl_result.setText('Peso: 0.000g')
                return

            metals_keys = ["Ouro_18k", "Ouro_14k", "Prata_925"]
            metal_key = metals_keys[self.choice]
            weight = self.calculator.calculate_weight(float(volume), metal_key)
            self.lbl_result.setText(f'Peso: {weight:.3f}g')
        except ValueError:
            QMessageBox.critical(self, "Erro", "Por favor, insira um valor numérico válido.")
            self.entry_volume.setFocus()

    def open_settings(self):
        """Abre a janela de configurações"""
        dialog = CalibrationDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """Lida com o fechamento da aplicação"""
        # Para a thread de atualização primeiro
        if self.gold_price_thread and self.gold_price_thread.isRunning():
            self.gold_price_thread.stop()
            # Aguarda no máximo GOLD_THREAD_TIMEOUT para a thread terminar
            if not self.gold_price_thread.wait(GOLD_THREAD_TIMEOUT):
                self.gold_price_thread.terminate()
        
        reply = QMessageBox.question(
            self,
            'Sair',
            'Deseja mesmo sair do programa?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_closing(self):
        """Fecha a aplicação"""
        self.close()
