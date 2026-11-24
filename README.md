# MNservidores — Investigação de Degradação de Desempenho em Servidores

Projeto desenvolvido para a disciplina de **Métodos Numéricos (2º GQ)** — **Problema 2: Investigação de Degradação de Desempenho em Servidores**.

O repositório organiza os métodos numéricos implementados do zero em Python puro (**Interpolação Polinomial de Lagrange** global/local e **Interpolação Polinomial de Newton via Diferenças Divididas**) em um pacote instalável via `pip` (`pacote_servidores`), utilizado em `notebook.ipynb` para analisar os episódios de degradação térmica nos servidores `SRV-01`, `SRV-02` e `SRV-03`.

---

## Integrantes do Grupo e Divisão de Funções

| Integrante | Responsabilidade | Arquivos Principais |
| :--- | :--- | :--- |
| **Carlos Gabryell** | Engenharia de Dados, leitura de CSV/log e normalização temporal | [`pacote_servidores/dados.py`](pacote_servidores/dados.py) |
| **Diego Kauã** | Interpolação Polinomial de Lagrange (global e local grau 3) | [`pacote_servidores/lagrange.py`](pacote_servidores/lagrange.py) |
| **Matheus** | Interpolação de Newton e Tabela de Diferenças Divididas | [`pacote_servidores/newton.py`](pacote_servidores/newton.py) |
| **Lucas Vinícius** | Cálculos nos incidentes, limite de 80 °C e análise de precisão (Itens a e b) | [`pacote_servidores/analise.py`](pacote_servidores/analise.py), [`notebook.ipynb`](notebook.ipynb) |
| **Moisés Freire** | Notebook, gráficos contínuos e diagnóstico técnico de infraestrutura (Itens c e d) | [`notebook.ipynb`](notebook.ipynb) |
| **Henry Lima** | Empacotamento (`pyproject.toml`), documentação (`README.md`), validação e apresentação PDF | [`pyproject.toml`](pyproject.toml), [`README.md`](README.md), [`apresentacao_problema2_servidores.pdf`](apresentacao_problema2_servidores.pdf) |

---

## Estrutura do Repositório

```text
MNservidores/
├── pyproject.toml                          # Configuração para instalação via pip
├── README.md                               # Instruções de instalação e uso
├── notebook.ipynb                          # Notebook que importa o pacote (Moisés Freire — itens a–d)
├── incidentes.log                          # Arquivo bruto de registro de incidentes
├── temperaturas.csv                        # Arquivo bruto de medições horárias (14h às 23h)
├── apresentacao_problema2_servidores.pdf   # Slides da apresentação (fundo branco para projeção)
└── pacote_servidores/                      # Pacote Python com os módulos do grupo
    ├── __init__.py                         # Marcador de pacote Python
    ├── dados.py                            # Leitura e tratamento de temperaturas.csv e incidentes.log
    ├── lagrange.py                         # Polinômios básicos Lk(x), Lagrange global e local
    ├── newton.py                           # Diferenças Divididas e polinômio de Newton
    └── analise.py                          # Execução da análise nos incidentes e verificação de 80 °C
```

---

## Requisitos

- **Python 3.11** ou superior
- **pip**
- **Jupyter** (ou extensão Jupyter no VS Code) para executar `notebook.ipynb`

---

## Instalação via `pip`

1. **Clone o repositório:**

```bash
git clone https://github.com/HenryDSLima/MNservidores.git
cd MNservidores
```

2. **Crie e ative um ambiente virtual (recomendado):**

- **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- **Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale o pacote com `pip`:**

```bash
pip install .
```

> Para desenvolvimento (modo editável), utilize `pip install -e .`.

As dependências declaradas em `pyproject.toml` (`matplotlib`, `numpy` e `ipykernel`) são instaladas automaticamente junto com o pacote `pacote_servidores`.

---

## Como Utilizar

### 1. Executando o Jupyter Notebook

Com o ambiente virtual ativo e o pacote instalado, abra e execute todas as células de `notebook.ipynb`:

```bash
jupyter notebook notebook.ipynb
```

O notebook importa as funções de `pacote_servidores` para carregar `temperaturas.csv` e `incidentes.log`, calcular as estimativas globais (grau 9) e locais (grau 3), exibir os gráficos contínuos e apresentar as respostas dos itens **(a)**, **(b)**, **(c)** e **(d)**.

### 2. Importando os Módulos em Python

```python
from pacote_servidores.dados import carregar_temperaturas, carregar_incidentes
from pacote_servidores.analise import executar_analise_servidores
from pacote_servidores.lagrange import lagrange, lagrange_local, pontos_do_servidor
from pacote_servidores.newton import tabela_diferencas_divididas, interpolar_newton

# Carregamento dos dados (14h00 -> t = 0.0h)
dados_servidores, referencia_inicial = carregar_temperaturas("temperaturas.csv")
incidentes = carregar_incidentes("incidentes.log", referencia_inicial)

# Análise nos horários dos incidentes (15:30, 18:30 e 21:30)
resultados, resultados_gerais = executar_analise_servidores(dados_servidores, incidentes)
for r in resultados:
    print(r)

# Exemplo de validação direta com o método de Newton (SRV-03 às 18:30, t = 4.5h)
pontos_srv3 = pontos_do_servidor(dados_servidores, "SRV-03")
xs = [p[0] for p in pontos_srv3]
ys = [p[1] for p in pontos_srv3]
print("Lagrange (G9):", lagrange(pontos_srv3, 4.5))
print("Newton   (G9):", interpolar_newton(xs, ys, 4.5))
```

---

## Resumo dos Resultados Obtidos

| Horário do Incidente | $t$ (h) | Servidor | Global (Grau 9) | Local (Grau 3) | Status (Limite 80 °C) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **15:30** | 1,5 | `SRV-01` | 48,48 °C | 49,24 °C | NORMAL |
| **15:30** | 1,5 | `SRV-02` | 57,48 °C | 57,26 °C | NORMAL |
| **15:30** | 1,5 | `SRV-03` | 61,41 °C | 61,14 °C | NORMAL |
| **18:30** | 4,5 | `SRV-01` | 48,03 °C | 48,32 °C | NORMAL |
| **18:30** | 4,5 | `SRV-02` | 61,36 °C | 61,26 °C | NORMAL |
| **18:30** | 4,5 | `SRV-03` | **81,03 °C** | **80,69 °C** | **CRÍTICO (Ultrapassou 80 °C)** |
| **21:30** | 7,5 | `SRV-01` | 48,47 °C | 49,05 °C | NORMAL |
| **21:30** | 7,5 | `SRV-02` | **77,07 °C** | **75,68 °C** | **ALERTA (Próximo de 80 °C)** |
| **21:30** | 7,5 | `SRV-03` | 61,87 °C | 61,17 °C | NORMAL |

- **SRV-03** é o único servidor a ultrapassar o limite operacional de **80 °C** às **18:30** (`81,03 °C` global / `80,69 °C` local), provável causa térmica da degradação no segundo incidente.
- **SRV-02** aproxima-se da zona crítica às **21:30** (`77,07 °C` global / `75,68 °C` local), sem superar 80 °C.
- **SRV-01** mantém-se estável entre `48,30 °C` e `51,37 °C` durante todo o período.

---

## Apresentação

Os slides da apresentação em formato PDF (fundo branco otimizado para projeção em datashow) estão disponíveis em [`apresentacao_problema2_servidores.pdf`](apresentacao_problema2_servidores.pdf).
