# Calculadora de Pesos de Metais - Versão 2.0

Aplicação desktop moderna para calcular pesos de metais preciosos com interface PySide6.

## 🎯 Características

- ✨ Interface moderna e responsiva com **PySide6**
- 📊 Cálculo automático de peso baseado em volume e tipo de metal
- 🔧 Calibração de densidades de metais
- 💰 Cotação de ouro atualizada em tempo real (BRL/USD)
- 🔄 Atualização automática de cotações a cada 60 segundos
- 💾 Cache robusto de cotações locais
- 🏗️ Arquitetura modular e bem documentada

## 📋 Requisitos

- Python 3.13+
- PySide6 6.8.1.1+
- requests 2.31.0+

## 🚀 Início Rápido

### Instalação

```bash
# Clonar ou baixar o repositório
cd Calcular_peso

# Instalar dependências
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
Calcular_peso/
├── src/                          # Código principal (nova arquitetura)
│   ├── config.py                 # Configurações centralizadas
│   ├── core/                     # Lógica de negócio
│   │   ├── calculator.py         # Cálculos de peso
│   │   └── gold_price.py         # Gerenciamento de cotações
│   ├── ui/                       # Interface do usuário
│   │   ├── main_window.py        # Janela principal
│   │   ├── dialogs/
│   │   │   └── calibration.py    # Diálogo de calibração
│   │   └── threads/
│   │       └── gold_price_thread.py  # Thread de atualização
│   └── utils/
│       └── paths.py              # Utilitários
├── main.py                       # Ponto de entrada
├── config.json                   # Arquivo de configuração
├── requirements.txt              # Dependências
├── ARCHITECTURE.md               # Documentação da arquitetura
├── CONTRIBUTING.md               # Guia de desenvolvimento
└── README.md                     # Este arquivo
```

## 🎮 Como Usar

1. **Abrir a aplicação**: Execute `python main.py`

2. **Inserir volume**: Digite o volume desejado no campo "Volume"

3. **Selecionar metal**: Clique no botão do metal desejado:
   - Ouro 18k
   - Ouro 14k
   - Prata 925

4. **Calcular**: Clique "Calcular" ou pressione Enter

5. **Ver resultado**: O peso será exibido em gramas

6. **Calibrar**: Menu "Configurações" > "Calibrar cálculo..." para ajustar densidades

## 📊 Funcionalidades

### Cálculo de Peso
- Baseado em volume (cm³) e densidade do metal
- Suporta entrada com ponto (.) ou vírgula (,)
- Resultados com precisão de 3 casas decimais

### Cotação de Ouro
- Exibida na barra de status (parte inferior)
- Cotação em Real (BRL) por grama
- Atualização automática a cada 60 segundos
- Indicadores: (BRL) = Atualizada | (Cache) = Local | (Padrão) = Valor fixo

### Calibração
- Ajuste de densidade de cada metal
- Valores salvos em `config.json`
- Botão para resetar valores padrão

## 🏗️ Arquitetura

A aplicação segue um padrão **modular em camadas**:

- **Camada de Configuração**: `config.py` centraliza todas as constantes
- **Camada de Negócio**: `core/` com lógica de cálculos e cotações
- **Camada de UI**: `ui/` com componentes de interface
- **Camada de Utilitários**: `utils/` com funções auxiliares

Veja [ARCHITECTURE.md](ARCHITECTURE.md) para mais detalhes.

## 📚 Guia de Desenvolvimento

Para contribuir ou estender a aplicação:

1. Leia [CONTRIBUTING.md](CONTRIBUTING.md)
2. Siga os padrões de código documentados
3. Mantenha a separação de camadas
4. Adicione docstrings a novas classes/funções

### Exemplos de Extensão

- **Adicionar novo metal**: Editar `src/config.py`
- **Adicionar nova API**: Criar método em `src/core/gold_price.py`
- **Criar novo diálogo**: Arquivo em `src/ui/dialogs/`

## 🔧 Compilar para Executável

### Com PyInstaller

```bash
# Cria executável único
pyinstaller --onefile --windowed --name "Calculadora Pesos" main.py

# Ou usar arquivo spec personalizado
pyinstaller main_spec.spec
```

## 📝 Configuração

### `config.json`
Armazena as densidades de metais:
```json
{
    "Ouro_18k": 15.5,
    "Ouro_14k": 14.0,
    "Prata_925": 10.5
}
```

### `src/config.py`
Define:
- Caminhos de arquivos
- Valores padrão
- Constantes da aplicação
- Timeouts e limites

## 🐛 Troubleshooting

**Problema**: Erro ao fechar a aplicação
**Solução**: Use versão 2.0 com thread corrigida

**Problema**: Cotação mostra "Indisponível"
**Solução**: Verifique conexão de internet, aplicação usa cache se offline

**Problema**: Erro de importação ao executar
**Solução**: Verifique se está na pasta correta e executou `pip install -r requirements.txt`

## 📄 Changelog

### v2.0 - Refatoração Arquitetônica
- ✅ Reorganização completa com arquitetura modular
- ✅ Separação em camadas (config, core, ui, utils)
- ✅ Melhora na manutenibilidade e testabilidade
- ✅ Documentação completa da arquitetura
- ✅ Correção de travamento ao fechar
- ✅ Thread de cotação melhorada

### v1.0 - Versão Inicial PySide6
- Interface PySide6 funcional
- Cálculos de peso
- Calibração de densidades
- Cotação de ouro

## 📄 Licença

Projeto mantido por JockaMt

## 📞 Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue ou entre em contato.

---

**Versão:** 2.0 (Refatorada)  
**Data:** 24 de outubro de 2025  
**Status:** ✅ Funcional e pronto para produção  
**Tecnologia:** PySide6 + Python 3.13
