# Análise e Priorização de Chamados 1746 – Rio de Janeiro

## Objetivo

Este projeto tem como objetivo analisar o comportamento dos chamados do serviço 1746 da cidade do Rio de Janeiro, incorporando fatores climáticos e territoriais, além de desenvolver um modelo preditivo para apoiar a priorização de atendimentos.

A análise busca responder principalmente:

* Como condições climáticas impactam a demanda por serviços urbanos?
* Quais regiões concentram maior volume de chamados?
* É possível prever o volume de chamados com base em variáveis estruturais, temporais e climáticas?


##  Estrutura do Projeto
```md
DESAFIO-CIENTISTA-DADOS-SENIOR/
│
├── data/
│   ├── chamados_1746.parquet
│   └── dim_territorio.parquet
│
├── models/
│   ├── staging/
│   │   ├── stg_chamado_1746.sql
│   │   ├── stg_dim_territorio.sql
│   │   └── schema.yml
│   │
│   └── intermediate/
│       ├── int_chamado_agrupado.sql
│       └── schema.yml
│
├── notebooks/
│   ├── 01_analise_apis_clima.ipynb
│   ├── 02_modelagem_resolucao.ipynb
│   ├── 03_sistema_priorizacao.ipynb
│   └── funcao_aux.py
│
├── target/
├── logs/
├── dbt_project.yml
├── README.md
└── dev.duckdb
```


## Organização das Camadas

### data/

Armazena os dados utilizados no projeto:

* Chamados do 1746
* Dimensão territorial (bairros, regiões, etc.)


### models/ (dbt)

Responsável pela transformação dos dados:

* **staging**

  * Limpeza
  * Padronização
  * Tipagem

* **intermediate**

  * Agregações
  * Regras de negócio
  * Consolidação dos dados para análise


### notebooks/

Contém as análises e modelagem:

* **01_analise_apis_clima.ipynb**

  * Integração com API climática (Open-Meteo)
  * Construção da base climática

* **02_modelagem_resolucao.ipynb**

  * Análise exploratória
  * Feature engineering
  * Treinamento e avaliação do modelo

* **03_sistema_priorizacao.ipynb**

  * Aplicação do modelo
  * Definição de lógica de priorização de chamados

* **funcao_aux.py**

  * Funções auxiliares reutilizáveis


## Execução do Projeto

### 1. Rodar transformação dos dados (dbt)

```bash
dbt run
```

### 2. Executar os notebooks na ordem:

1. `01_analise_apis_clima.ipynb`
2. `02_modelagem_resolucao.ipynb`
3. `03_sistema_priorizacao.ipynb`


##  Principais Insights

* A demanda por chamados está fortemente associada à **estrutura territorial**, representando cerca de **76% da importância do modelo**.
* Variáveis temporais (dia da semana, mês) possuem impacto relevante, porém secundário (~16%).
* Fatores climáticos (temperatura e precipitação) atuam como elementos complementares (~7%).
* A composição dos tipos de chamados se mantém estável, independentemente do tipo de dia (normal, feriado ou evento extremo).
* Feriados apresentam redução significativa na demanda, indicando menor intensidade de uso urbano.


## Modelo Preditivo

Foi desenvolvido um modelo de machine learning capaz de prever o volume de chamados com base em variáveis:

* Territoriais
* Temporais
* Climáticas

### Performance

* **R²:** ~0.82
* **MAE:** ~5.9
* **RMSE:** ~11.2

O modelo apresentou boa capacidade de generalização e captura dos padrões da demanda.


## Interpretação do Modelo

O modelo evidencia que:

* A **localização geográfica** é o principal fator explicativo da demanda
* Variáveis climáticas influenciam, mas não determinam o comportamento
* A demanda está mais relacionada à **intensidade de uso da cidade** do que a fatores isolados

## Considerações Finais

Os resultados mostram que a priorização de atendimentos pode ser aprimorada ao considerar:

* Concentração territorial da demanda
* Padrões temporais
* Condições climáticas

Essa abordagem permite uma visão mais estratégica da operação urbana, apoiando decisões mais eficientes na alocação de recursos.
