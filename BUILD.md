# 🔨 Guia de Build

## Build para Windows (.exe)

### 1. Preparar o Ambiente

```bash
# Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Executar o Build

#### Opção A: Build Simples (Recomendado)

```bash
pyinstaller app.spec
```

A aplicação executável estará em: `dist/Calculadora_Pesos.exe`

#### Opção B: Build Com Ícone

1. Prepare um arquivo `icone.ico` na raiz do projeto
2. Edite `app.spec` e descomente: `icon=icon_path`
3. Execute:
   ```bash
   pyinstaller app.spec
   ```

#### Opção C: Build Sem Spec (Manual)

```bash
pyinstaller --onefile --windowed --name "Calculadora_Pesos" main.py
```

### 3. Distribuir

```bash
# O executável está em:
dist/Calculadora_Pesos.exe

# Para distribuir, copie apenas este arquivo
# Todos os arquivos necessários estão inclusos
```

## Limpeza

```bash
# Remover arquivos de build
rmdir /s build dist
del *.spec  # Se não estiver usando spec file
```

## Troubleshooting

### Erro: "Failed to execute script main"
- Verifique se `main.py` está na raiz do projeto
- Verifique se `src/` tem todos os arquivos necessários
- Teste executando `python main.py` antes do build

### Erro: "No module named 'PySide6'"
- Certifique-se que `pyinstaller` foi feito com o mesmo Python
- Use: `pip install pyinstaller PySide6`

### Executável muito grande
- Normal! PySide6 é pesado (~500MB em dist/)
- Use `--onefile` para reduzir se necessário

## Verificação Pre-Build

Execute antes de fazer build:

```bash
# Verificar arquitetura
python verify_architecture.py

# Testar aplicação
python main.py
```

## Specs Diferentes para Diferentes Cenários

### Para Usuários (Com Console)
```bash
pyinstaller --onefile --console --name "Calculadora_Pesos" main.py
```

### Para Servidor/Batch
```bash
pyinstaller --onefile --console main.py
```

### Para Distribuição (Sem Arquivo Extrator)
```bash
pyinstaller --onedir --windowed --name "Calculadora_Pesos" main.py
```

---

**Último Update:** 24 de outubro de 2025
