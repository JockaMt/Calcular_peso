# 📁 Estrutura do Projeto - Calculadora de Pesos de Metais v2.0

```
Calcular_peso/
│
├── 📄 main.py                      # Ponto de entrada da aplicação
│
├── 🔧 src/                         # Código-fonte principal
│   ├── __init__.py
│   ├── config.py                   # Configurações centralizadas
│   │
│   ├── core/                       # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── calculator.py           # Cálculos de peso
│   │   └── gold_price.py           # Gerenciamento de cotações
│   │
│   ├── ui/                         # Interface do usuário
│   │   ├── __init__.py
│   │   ├── main_window.py          # Janela principal
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   └── calibration.py      # Diálogo de calibração
│   │   └── threads/
│   │       ├── __init__.py
│   │       └── gold_price_thread.py # Thread de atualização
│   │
│   └── utils/
│       ├── __init__.py
│       └── paths.py                # Utilitários
│
├── 📦 Distribuição
│   ├── app.spec                    # Spec file PyInstaller
│   ├── BUILD.md                    # Guia de build
│   └── requirements.txt            # Dependências Python
│
├── 📚 Documentação
│   ├── README.md                   # README principal
│   ├── README_v2.md                # README detalhado v2
│   ├── ARCHITECTURE.md             # Documentação arquitetura
│   ├── CONTRIBUTING.md             # Guia desenvolvimento
│   ├── REFACTORING_SUMMARY.md      # Sumário refatoração
│   ├── PROJECT_STRUCTURE.md        # Este arquivo
│   └── BUILD.md                    # Instruções build
│
├── ⚙️ Configuração
│   ├── config.json                 # Densidades de metais
│   ├── .gitignore                  # Git ignore
│   └── requirements.txt            # Dependências
│
├── 🧪 Desenvolvimento
│   ├── verify_architecture.py      # Script verificação
│   └── .git/                       # Repositório Git
│
└── ⚠️ Legado (removido)
    ├── calculo.py                  # ❌ Removido
    ├── menu/                       # ❌ Removido
    ├── main.spec                   # ❌ Removido
    ├── test_close.py               # ❌ Removido
    ├── build/                      # ❌ Removido
    ├── dist/                       # ❌ Removido
    ├── __pycache__/                # ❌ Removido
    └── db/                         # ❌ Removido
```

## 📊 Componentes Principais

### Core (Lógica de Negócio)
- `Calculator`: Cálculos de peso
- `GoldPriceManager`: Gerenciamento de cotações

### UI (Interface)
- `MainWindow`: Janela principal
- `CalibrationDialog`: Diálogo de calibração
- `GoldPriceThread`: Thread de atualização

### Configuração
- `config.py`: Centraliza todas as constantes
- `config.json`: Densidades de metais

## 📈 Tamanho do Projeto

```
Código Fonte (src/):     ~600 linhas
Documentação:            ~500 linhas
Configuração:            ~100 linhas
Total:                   ~1.200 linhas
```

## 🗂️ Organização de Pastas

### src/
- **config.py**: Ponto único de configuração
- **core/**: Lógica de negócio isolada
- **ui/**: Componentes de interface
- **utils/**: Funções auxiliares

### Benefícios
✅ Fácil localizar código  
✅ Fácil adicionar novos recursos  
✅ Fácil testar isoladamente  
✅ Escalável para crescimento  

## 🔄 Fluxo de Dados

```
Usuário
   ↓
MainWindow (UI)
   ↓
├── Calculator (core)
│   └── config.json
│
└── GoldPriceManager (core)
    └── API / Cache / Padrão
```

## 📦 Dependências

### Produção
- `PySide6`: Interface gráfica
- `requests`: Requisições HTTP

### Build (Opcional)
- `pyinstaller`: Criar executável

## 🚀 Próximos Passos

1. **Testes Unitários**
   ```
   tests/
   ├── test_calculator.py
   ├── test_gold_price.py
   └── test_main_window.py
   ```

2. **CI/CD Pipeline**
   ```
   .github/
   └── workflows/
       ├── test.yml
       └── build.yml
   ```

3. **Tradução (i18n)**
   ```
   locales/
   ├── pt_BR.json
   ├── en_US.json
   └── es_ES.json
   ```

4. **Ícone e Assets**
   ```
   assets/
   ├── icon.ico
   ├── logo.png
   └── screenshots/
   ```

## 📋 Checklist de Limpeza

- ✅ Removido `calculo.py` (legado)
- ✅ Removido pasta `menu/` (legado)
- ✅ Removido `main.spec` (substituído por app.spec)
- ✅ Removido `test_close.py` (teste único)
- ✅ Removido cache (`__pycache__/`)
- ✅ Removido build artifacts (`build/`, `dist/`)
- ✅ Adicionado `.gitignore` completo
- ✅ Otimizado `requirements.txt`
- ✅ Criado `app.spec` moderno

## 🎯 Status do Projeto

| Aspecto | Status | Nota |
|---------|--------|------|
| Código | ✅ | Pronto produção |
| Testes | ⏳ | Próximo passo |
| Docs | ✅ | Completa |
| Build | ✅ | Pronto |
| Deploy | ✅ | Pronto |

---

**Estrutura Criada:** 24 de outubro de 2025  
**Versão:** 2.0  
**Status:** ✅ Pronto para Produção e Deploy
