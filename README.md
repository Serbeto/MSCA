# MSCA - Módulo de Simulação de Curto-Circuito em Análise de Sistemas Elétricos

Este projeto é um simulador de análise de **curto-circuito em sistemas elétricos**, capaz de avaliar **diversos tipos de faltas** (trifásica, bifasica, bifasica-terra e monofasica). O objetivo é fornecer uma ferramenta flexível para estudos de transitórios e análise de comportamento do sistema em diferentes condições de falha.

## ⚙️ Estrutura base

Um dos pilares do programa é a **formação da matriz Ybarra** (matriz de admitância nodal) por meio da **soma das submatrizes de admitância** de cada componente do sistema:

- Linhas de transmissão
- Transformadores (com diferentes configurações de conexão)
- Geradores (com ou sem aterramento na sequência zero)

Essa abordagem modular permite uma construção clara e extensível da matriz para cada sequência (positiva, negativa e zero).

## ⚡ Funcionalidades principais

- Leitura e organização de dados via terminal.
- Cálculo das matrizes Ybarra e Zbarra para cada sequência.
- Suporte completo a:
  - Curto-circuito trifásico
  - Bifásico
  - Monofásico
  - Bifásico com terra
- Análise de tensões e correntes durante as faltas.
- Definição automática das áreas do sistema elétrico, considerando transformadores e topologia.
- Identificação e ajuste de defasagens por conexões Y-Δ e Δ-Y.

## 🧪 Como executar

1. Certifique-se de ter o Python instalado (>= 3.8).
2. Clone o repositório:

```bash
git clone https://github.com/Serbeto/MSCA.git
cd MSCA
