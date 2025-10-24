# 📐 Layout da Interface - Calculadora de Pesos de Metais

## 🎨 Estrutura Visual

```
╔════════════════════════════════════════════════════════════╗
║  Calculadora de Pesos de Metais       [_] [□] [X]         ║
╠════════════════════════════════════════════════════════════╣
║ Menu  ⚙️ Configurações                                      ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  Volume:  [_____________]  [Calcular]                      ║
║                                                             ║
║  [Ouro 18k]  [Ouro 14k]  [Prata 925]                      ║
║                                                             ║
║  Peso: 0.000g                          [⚙️ Calibrar]       ║
║                                                             ║
╠════════════════════════════════════════════════════════════╣
║ Cotação do Ouro: R$ 713,38/g (BRL)  [melhorcambio]        ║
╚════════════════════════════════════════════════════════════╝
```

## 🔧 Componentes Principais

### 1️⃣ Barra de Menu (Topo)
- **Configurações**
  - Calibrar cálculo...
  - ─────────────
  - Sair

### 2️⃣ Seção de Entrada
- **Campo Volume**: Input numérico com Enter para calcular
- **Botão Calcular**: Dispara o cálculo
- Layout horizontal (esquerda para direita)

### 3️⃣ Seção de Seleção de Metal
- **Botões de Opção**:
  - Ouro 18k (padrão)
  - Ouro 14k
  - Prata 925
- Layout horizontal com distribuição uniforme
- Apenas um pode estar ativo por vez

### 4️⃣ Seção de Resultado
- **Exibição do Peso**: Bold, fonte 10pt
- **Botão de Calibração** ⭐ NOVO
  - Posicionado à direita
  - Ícone ⚙️ com texto "Calibrar"
  - Acesso rápido sem menu
- Layout horizontal com espaçamento

### 5️⃣ Barra de Status (Rodapé)
- **Cotação do Ouro em Tempo Real**
  - Atualiza a cada 60 segundos
  - Mostra fonte: `(melhorcambio)`, `(cache)`, ou `(padrão)`
  - Formato: `R$ XXX,XX/g (BRL)`

## 📍 Posição do Botão de Configurações

### ANTES (Apenas no Menu)
```
Menu → Configurações → Calibrar cálculo...
```
- ❌ Menos visível
- ❌ Requer mais cliques

### DEPOIS (Menu + Botão Principal)
```
Menu → Configurações → Calibrar cálculo...  [Visível mas profundo]
                                             +
Interface Principal → [⚙️ Calibrar]  [Visível e acessível]
```
- ✅ Fácil acesso na janela principal
- ✅ Ícone intuitivo (⚙️)
- ✅ Posicionado logicamente após o resultado
- ✅ Menu ainda disponível para usuários avançados

## 🎯 Fluxo de Uso

### Cenário 1: Cálculo Simples
```
1. Abrir aplicação
2. Inserir Volume
3. Clicar "Calcular" (ou pressionar Enter)
4. Ver resultado
5. Fechar
```

### Cenário 2: Ajustar Densidades
```
1. Abrir aplicação
2. Clicar [⚙️ Calibrar] ← NOVO, rápido acesso
3. Modificar valores
4. Salvar e voltar
5. Calcular com novos valores
```

### Cenário 3: Menu Completo
```
1. Clicar "Configurações" na barra de menu
2. Selecionar "Calibrar cálculo..."
3. OU Selecionar "Sair"
```

## 🎨 Dimensões

- **Janela Principal**: 500px × 300px
- **Fonte Padrão**: System (Qt Default)
- **Fonte Resultado**: Bold, 10pt
- **Botão Calibrar**: Max-width 120px
- **Espaçamento**: 10px (margens), 10px (entre componentes)

## 🔄 Estados dos Botões

### Seleção de Metal
- **Ativo**: Background colorido, texto em negrito
- **Inativo**: Background neutro

### Botão Calibrar
- **Normal**: Ícone ⚙️ + Texto "Calibrar"
- **Hover**: Destaque visual
- **Clique**: Abre `CalibrationDialog`

## 📱 Responsividade

- Layout em colunas (VBoxLayout)
- Componentes horizontais (HBoxLayout)
- Espaçamento com `addStretch()` para distribuição automática
- Janela fixa: 500x300px (sem redimensionamento)

## ✨ Melhorias Implementadas

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Acesso Configurações | Menu (2 cliques) | Botão direto (1 clique) |
| Visibilidade | Apenas no menu | Menu + Botão principal |
| Usabilidade | Menos óbvio | Intuitivo com ícone |
| Layout | Resultado simples | Resultado + Controle |
| Hierarquia | Linear | Visual com espaçamento |

## 🚀 Próximas Melhorias Sugeridas

1. Atalho de teclado (Ctrl+Shift+S) para calibração
2. Tooltip no botão calibrar
3. Indicador visual se densidades foram modificadas
4. Tema escuro/claro (toggle)
5. Histórico de cálculos

---

**Status**: ✅ Botão de configurações agora está visível e acessível na interface principal
**Última atualização**: 24 de outubro de 2025
