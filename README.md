# 📊 Sistema de Análise de Vendas - Óleo, Açúcar e Leite

## 🎯 Visão Geral

Sistema simples e direto para análise de vendas e gestão de compras dos produtos **Óleo**, **Açúcar** e **Leite**. O sistema mostra apenas o essencial: **vendas e compras recomendadas por subgrupo**, tanto de forma geral quanto separada por loja.

## ✨ O que o Sistema Mostra

### 📊 1. Análise Geral por Subgrupo
- **Vendas** de cada categoria (Óleo, Açúcar, Leite) em unidades
- **Compras recomendadas** para cada categoria em unidades
- **Gráficos simples** de vendas e compras

### 🏪 2. Análise por Loja
- **Vendas** de cada categoria por loja em unidades
- **Compras recomendadas** por loja e categoria em unidades
- **Tabelas organizadas** por loja

### 📁 3. Exportação Simples
- **CSV do resumo geral** por subgrupo
- **CSV dos dados por loja**

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Interface web interativa
- **Pandas** - Manipulação e análise de dados
- **Plotly Express** - Geração de gráficos interativos
- **SQLite** - Banco de dados interno
- **NumPy** - Suporte a operações numéricas

## ⚙️ Configurações

### Parâmetros de Análise
- **Período de análise:** 21 dias (configurável de 7 a 90 dias)
- **Período de projeção:** 15 dias (configurável de 1 a 60 dias)
- **Unidade de medida:** Unidades (un)

## 🎯 Como Usar

### Localmente:
1. Execute `streamlit run dashboard.py`
2. Configure o período no painel lateral
3. Clique em "Gerar Análise Completa"
4. Visualize vendas e compras por subgrupo

### Online (Deploy):
1. Acesse: https://acucar-leite-oleo-8xkxt4rahmvpgppqrvumsu.streamlit.app/
2. Configure os parâmetros
3. Clique em "Gerar Análise Completa"
4. Use os dados simulados

## 📊 Exemplo de Resultados

### Análise Geral por Subgrupo:
| Subgrupo | Vendas (un) | Comprar (un) |
|----------|-------------|--------------|
| ÓLEO     | 2.058       | 450          |
| AÇÚCAR   | 3.180       | 680          |
| LEITE    | 4.450       | 920          |

### Análise por Loja:
- **Loja 1**: Óleo (250 un vendas, 50 un comprar), Açúcar (500 un vendas, 100 un comprar)
- **Loja 2**: Óleo (300 un vendas, 75 un comprar), Açúcar (400 un vendas, 80 un comprar)

## 🔒 Segurança

- Banco interno SQLite (sem dados sensíveis)
- **Cache de dados** por 5 minutos para performance
- **Dados simulados** para demonstração

## 📁 Estrutura do Projeto

```
├── dashboard.py           # App principal
├── database_manager.py    # Gerenciador do banco SQLite
├── atualizar_dados.py     # Script de atualização
├── agendar_atualizacao.bat/sh  # Agendadores
├── dados_vendas.db        # Banco SQLite
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```