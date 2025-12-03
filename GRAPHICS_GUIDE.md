# 📊 Guia Educacional - Gráficos e Conceitos Estatísticos

**Um guia didático para entender as visualizações do Energy Analytics Dashboard**

---

## 📚 Índice

1. [Gráficos Implementados](#gráficos-implementados)
2. [Conceitos Estatísticos](#conceitos-estatísticos)
3. [Detecção de Anomalias](#detecção-de-anomalias)
4. [Interpretação de Visualizações](#interpretação-de-visualizações)
5. [Glossário](#glossário)

---

## 🎨 Gráficos Implementados

### 1. Gráfico Dual-Axis (Dois Eixos)

**O que é:**
Um gráfico que combina duas séries temporais com escalas diferentes no mesmo espaço visual.

**No nosso dashboard:**
- **Eixo Esquerdo (Azul)**: Carga energética em MW (Megawatts)
- **Eixo Direito (Vermelho)**: Temperatura em °C (Graus Celsius)

**Por que é útil:**
Permite visualizar a relação entre duas variáveis com unidades diferentes. No nosso caso, vemos como a temperatura influencia o consumo de energia.

**Como interpretar:**
```
📈 Picos de carga azul + picos de temperatura vermelha = Correlação positiva
   (Mais calor → Mais uso de ar condicionado → Mais consumo)

📉 Vales simultâneos = Dias mais frios, menos consumo
```

**Exemplo Real:**
```
Verão (Jan-Mar):
- Temperatura: 28-30°C (linha vermelha alta)
- Carga: 45,000 MW (linha azul alta)
→ Forte uso de climatização

Inverno (Jun-Ago):
- Temperatura: 15-18°C (linha vermelha baixa)
- Carga: 35,000 MW (linha azul mais baixa)
→ Menor demanda energética
```

---

### 2. Gráfico com Bandas de Confiança (Confidence Bands)

**O que é:**
Um gráfico de série temporal com faixas que mostram o intervalo "normal" de valores esperados.

**Componentes:**
1. **Linha Azul Sólida**: Valores reais medidos
2. **Linha Tracejada Cinza**: Média (μ)
3. **Banda Escura**: ±1σ (sigma) - 68% dos dados
4. **Banda Clara**: ±2σ (sigma) - 95% dos dados

**Conceito Matemático:**

```
σ (sigma) = Desvio Padrão
μ (mu) = Média

Banda ±1σ: [μ - σ, μ + σ]    → 68% dos dados
Banda ±2σ: [μ - 2σ, μ + 2σ]  → 95% dos dados
Banda ±3σ: [μ - 3σ, μ + 3σ]  → 99.7% dos dados
```

**Como interpretar:**
- **Dentro de ±1σ**: Valores normais
- **Entre ±1σ e ±2σ**: Valores incomuns, mas não alarmantes
- **Fora de ±2σ**: Possíveis anomalias (apenas 5% dos casos)
- **Fora de ±3σ**: Anomalias claras (0.3% dos casos)

**Exemplo Visual:**
```
     ┌─────────────────────────────────┐
52K ─┤                            ○    │ ← Anomalia (fora de ±2σ)
     │        Banda ±2σ (clara)        │
48K ─┤    ................................│
     │    ┌──────────────────────────┐ │
44K ─┤    │   Banda ±1σ (escura)    │ │
     │    │  ┌─── Média ────┐       │ │
40K ─┤────┼──┼───────────────┼───────┼─│
     │    │  │ Valores normais│      │ │
36K ─┤    │  └────────────────┘      │ │
     │    └──────────────────────────┘ │
32K ─┤    ................................│
     └─────────────────────────────────┘
```

---

### 3. Box Plot (Diagrama de Caixa)

**O que é:**
Visualização que mostra a distribuição estatística de um conjunto de dados.

**Componentes:**
```
    ┌─── Outliers (valores extremos)
    │
    ●  ← Máximo (Q3 + 1.5×IQR)
    │
    ┬── Q3 (75º percentil - 3º quartil)
    │
    ┤   ← Mediana (50º percentil - Q2)
    │
    ┴── Q1 (25º percentil - 1º quartil)
    │
    ●  ← Mínimo (Q1 - 1.5×IQR)
    │
    └─── Outliers
```

**Conceitos:**
- **Mediana (Q2)**: Valor do meio - 50% dos dados estão abaixo
- **Q1 (1º Quartil)**: 25% dos dados estão abaixo
- **Q3 (3º Quartil)**: 75% dos dados estão abaixo
- **IQR (Interquartile Range)**: Q3 - Q1 (amplitude interquartil)
- **Outliers**: Valores fora de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]

**Como interpretar:**
```
Caixa grande = Alta variabilidade
Caixa pequena = Baixa variabilidade
Mediana no centro = Distribuição simétrica
Mediana deslocada = Distribuição assimétrica
Muitos outliers = Dados com extremos frequentes
```

**Exemplo Real (Sudeste vs Sul):**
```
Sudeste:                     Sul:
   ┬ 52K (máx)                  ┬ 17K (máx)
   ┤ 45K (Q3)                   ┤ 14K (Q3)
   ┤ 42K (mediana)              ┤ 12.5K (mediana)
   ┤ 39K (Q1)                   ┤ 11K (Q1)
   ┴ 31K (mín)                  ┴ 8.5K (mín)

Interpretação:
- Sudeste: Maior consumo, alta variabilidade
- Sul: Menor consumo, mais estável
```

---

### 4. Heatmap de Correlação

**O que é:**
Matriz visual que mostra a força da relação entre pares de variáveis.

**Escala de Cores:**
```
🔴 Vermelho Escuro (+1.0): Correlação positiva perfeita
🔴 Vermelho Claro (+0.7):  Correlação positiva forte
⚪ Branco (0.0):          Sem correlação
🔵 Azul Claro (-0.7):     Correlação negativa forte
🔵 Azul Escuro (-1.0):    Correlação negativa perfeita
```

**Conceito de Correlação:**
```
Correlação (r) mede a relação linear entre duas variáveis

r = +1.0: Relação perfeita positiva (↑A → ↑B)
r = +0.7: Relação forte positiva
r = +0.3: Relação fraca positiva
r =  0.0: Sem relação
r = -0.3: Relação fraca negativa
r = -0.7: Relação forte negativa
r = -1.0: Relação perfeita negativa (↑A → ↓B)
```

**⚠️ IMPORTANTE:**
> **Correlação ≠ Causalidade**
>
> Uma correlação forte não significa que A causa B!
> Pode haver uma terceira variável (confusora) ou coincidência.

**Exemplo Real:**
```
Carga vs Temperatura: r = +0.696
↑ Temperatura → ↑ Carga (forte correlação)
Interpretação: Dias mais quentes tendem a ter maior consumo
Causa provável: Uso de ar condicionado
```

---

### 5. Scatter Plot de Anomalias

**O que é:**
Gráfico de dispersão que marca visualmente valores anormais.

**Componentes:**
- **Pontos Azuis (●)**: Valores normais
- **X Vermelhos (✕)**: Anomalias detectadas

**Como funcionam as anomalias:**
```
Z-score = (valor - média) / desvio_padrão

Z-score > +2.5 → Valor muito acima do esperado
Z-score < -2.5 → Valor muito abaixo do esperado
```

**Interpretação:**
```
Ponto em (15/11/2023, Z=2.8):
→ Data: 15 de novembro de 2023
→ Z-score: 2.8 (2.8 desvios padrão acima da média)
→ Probabilidade: ~0.5% de ocorrer naturalmente
→ Conclusão: Evento anormal, investigar causa
```

---

## 📐 Conceitos Estatísticos

### 1. Média (μ - Mu)

**Definição:**
Soma de todos os valores dividida pela quantidade.

**Fórmula:**
```
μ = (x₁ + x₂ + ... + xₙ) / n
```

**Exemplo:**
```
Cargas: 10K, 12K, 11K, 13K, 14K MW
Média = (10 + 12 + 11 + 13 + 14) / 5 = 12K MW
```

**Quando usar:**
- Dados simétricos (distribuição normal)
- Sem outliers extremos

**Limitação:**
Sensível a outliers (valores extremos distorcem a média)

---

### 2. Mediana

**Definição:**
Valor central quando dados estão ordenados.

**Como calcular:**
```
Dados ordenados: 10, 11, 12, 13, 14
            Mediana →  12  ← Valor central
```

**Vantagem:**
Não é afetada por outliers

**Exemplo:**
```
Com outlier:
Cargas: 10K, 11K, 12K, 13K, 100K MW
Média = 29.2K MW  ← Distorcida pelo outlier
Mediana = 12K MW  ← Representa melhor o "típico"
```

---

### 3. Desvio Padrão (σ - Sigma)

**Definição:**
Medida de dispersão - quanto os dados variam em relação à média.

**Fórmula:**
```
σ = √[Σ(xᵢ - μ)² / n]
```

**Interpretação:**
```
σ pequeno (ex: 100): Dados concentrados, pouca variação
σ grande (ex: 5000): Dados espalhados, alta variação
```

**Exemplo Visual:**
```
Baixo σ:             Alto σ:
    ┊                  ┊
  ┊┊┊┊┊              ┊ ┊ ┊ ┊ ┊
 ┊┊┊┊┊┊┊           ┊  ┊ ┊ ┊  ┊
┊┊┊┊┊┊┊┊┊         ┊   ┊ ┊ ┊   ┊
───────────       ─────────────────
(μ = 12K)         (μ = 12K)
```

---

### 4. Z-Score (Escore Padronizado)

**Definição:**
Quantos desvios padrão um valor está da média.

**Fórmula:**
```
Z = (x - μ) / σ
```

**Interpretação:**
```
Z = 0:    Exatamente na média
Z = +1:   1 desvio padrão acima (comum)
Z = +2:   2 desvios acima (incomum)
Z = +2.5: 2.5 desvios acima (anomalia)
Z = +3:   3 desvios acima (muito raro)
Z = -2.5: 2.5 desvios abaixo (anomalia)
```

**Exemplo Prático:**
```
Dado:
- Média (μ) = 12,000 MW
- Desvio (σ) = 2,000 MW
- Valor observado = 17,000 MW

Cálculo:
Z = (17,000 - 12,000) / 2,000 = 2.5

Interpretação:
17,000 MW está 2.5 desvios acima da média
→ Anomalia detectada!
```

---

### 5. Correlação (r - Coeficiente de Pearson)

**Definição:**
Mede a força e direção da relação linear entre duas variáveis.

**Fórmula (simplificada):**
```
r = Cov(X,Y) / (σₓ × σᵧ)

Onde:
- Cov(X,Y) = Covariância entre X e Y
- σₓ, σᵧ = Desvios padrão de X e Y
```

**Classificação:**
```
|r| = 0.0 - 0.3: Fraca
|r| = 0.3 - 0.7: Moderada
|r| = 0.7 - 1.0: Forte
```

**Exemplos Visuais:**
```
r = +0.9 (forte positiva):
Y │     ●
  │    ●
  │   ●
  │  ●
  │ ●
  └──────── X

r = -0.9 (forte negativa):
Y │ ●
  │  ●
  │   ●
  │    ●
  │     ●
  └──────── X

r = 0.0 (sem correlação):
Y │ ●  ●
  │   ●  ●
  │ ●  ●
  │  ●  ●
  └──────── X
```

---

## 🚨 Detecção de Anomalias

### Método Usado: Z-Score

**Por que Z-score?**
1. Simples de calcular
2. Funciona bem com distribuições normais
3. Threshold interpretável (2.5σ = 98.7% de confiança)

**Regra de Detecção:**
```python
if abs(Z-score) > 2.5:
    classificar_como_anomalia()
```

**Probabilidades:**
```
|Z| > 1.0: 31.7% dos dados (comum)
|Z| > 2.0:  4.6% dos dados (incomum)
|Z| > 2.5:  1.2% dos dados (raro) ← Nosso threshold
|Z| > 3.0:  0.3% dos dados (muito raro)
```

### Tipos de Anomalias

**1. Pico de Demanda:**
```
Z-score: +2.8
Interpretação: Consumo muito acima do esperado
Causas possíveis:
- Onda de calor
- Evento especial (jogo, feriado)
- Falha em outra região (transferência de carga)
```

**2. Queda Anormal:**
```
Z-score: -2.6
Interpretação: Consumo muito abaixo do esperado
Causas possíveis:
- Feriado com comércio fechado
- Problema no sistema de medição
- Apagão parcial
```

---

## 🎯 Interpretação de Visualizações

### Cenário 1: Analisando Sazonalidade

**Observação no Gráfico:**
```
Verão: Carga = 45K MW, Temp = 30°C
Inverno: Carga = 35K MW, Temp = 15°C
```

**Análise:**
1. Identificar padrão: Correlação positiva
2. Calcular amplitude: 45K - 35K = 10K MW (28% variação)
3. Conclusão: Forte dependência sazonal

**Ações:**
- Planejamento de manutenção no inverno (menor demanda)
- Preparação extra no verão (picos esperados)

---

### Cenário 2: Comparando Regiões

**Observação no Box Plot:**
```
Sudeste: Mediana = 42K, IQR = 6K (caixa grande)
Sul:     Mediana = 12K, IQR = 3K (caixa pequena)
```

**Análise:**
1. Sudeste: Maior consumo + maior variabilidade
   → Região industrializada, dependente de clima
2. Sul: Menor consumo + mais estável
   → Matriz energética diversificada ou clima estável

---

### Cenário 3: Investigando Anomalia

**Observação:**
```
Data: 17/11/2023
Região: Sudeste/CO
Carga: 53,717 MW
Z-score: +2.86
Temp: 28.8°C
```

**Processo de Investigação:**
1. **Validar dados**: Não é erro de medição?
2. **Contexto temporal**: Que dia da semana? Feriado?
3. **Contexto climático**: Onda de calor? Comparar com outros dias
4. **Contexto regional**: Outras regiões também anormais?
5. **Decisão**: Anomalia real ou evento planejado?

---

## 📖 Glossário

### Termos Estatísticos

| Termo | Símbolo | Significado |
|-------|---------|-------------|
| **Média** | μ (mu) | Valor central (soma/n) |
| **Mediana** | Q2 | Valor do meio (50º percentil) |
| **Moda** | - | Valor mais frequente |
| **Desvio Padrão** | σ (sigma) | Dispersão dos dados |
| **Variância** | σ² | Quadrado do desvio padrão |
| **Z-Score** | Z | Desvios padrão da média |
| **Correlação** | r | Força da relação (-1 a +1) |
| **Quartil** | Q1, Q2, Q3 | Divisão em 4 partes (25%, 50%, 75%) |
| **IQR** | Q3-Q1 | Amplitude interquartil |
| **Outlier** | - | Valor extremo/anormal |

### Termos Energéticos

| Termo | Unidade | Significado |
|-------|---------|-------------|
| **Carga** | MW | Demanda energética instantânea |
| **Energia** | MWh | Potência × tempo |
| **Pico de demanda** | MW | Maior carga do período |
| **Subsistema** | - | Região interligada (N, NE, S, SE/CO) |

---

## 🎓 Para Aprender Mais

### Livros Recomendados
1. **Estatística Básica**: Morettin & Bussab
2. **Data Visualization**: Edward Tufte
3. **Time Series Analysis**: Box & Jenkins

### Cursos Online
- Khan Academy: Estatística e Probabilidade
- Coursera: Data Visualization (University of Illinois)
- edX: Introduction to Statistics (UC Berkeley)

### Ferramentas
- **Plotly**: Documentação oficial
- **Pandas**: Guide de estatísticas descritivas
- **SciPy**: Statistical functions

---

## 📝 Exercícios Práticos

### Exercício 1: Interpretação de Z-Score
```
Dado:
- Média de carga: 20,000 MW
- Desvio padrão: 3,000 MW
- Valor observado: 26,500 MW

Questão: Este valor é uma anomalia (threshold = 2.5)?

Solução:
Z = (26,500 - 20,000) / 3,000 = 2.17
Resposta: Não (Z < 2.5), mas é incomum
```

### Exercício 2: Interpretação de Correlação
```
Correlação Carga × Precipitação: r = -0.35

Questão: O que isso significa?

Resposta:
- Correlação negativa fraca
- Dias chuvosos tendem a ter ligeiramente menor consumo
- Relação existe, mas outros fatores são mais importantes
```

---

**Criado:** 2025-12-03
**Versão:** 1.0
**Público:** Estudantes, analistas e usuários do dashboard

---

<div align="center">

**📊 Energy Analytics Dashboard**

*Entenda seus dados, tome melhores decisões*

</div>
