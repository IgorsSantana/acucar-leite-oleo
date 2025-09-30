# 📊 Sistema de Análise Simplificada de Vendas

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
- **Plotly** - Visualizações interativas
- **PyODBC** - Conexão com banco de dados IBM DB2
- **NumPy** - Cálculos numéricos
- **XlsxWriter** - Exportação para Excel

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Driver IBM DB2 ODBC instalado
- Acesso ao banco de dados SAB

### Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd oleo-acucar-leite
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o dashboard (Recomendado):**
```bash
streamlit run dashboard.py
```

4. **Ou execute a aplicação desktop:**
```bash
python app.py
```

## 📊 Produtos Analisados

| Categoria | Código Subgrupo | Descrição |
|-----------|----------------|-----------|
| 🛢️ Óleo | 211604 | Óleos comestíveis diversos |
| 🥛 Leite | 410204 | Leite e derivados |
| 🍯 Açúcar | 210604 | Açúcar e adoçantes |

## 🔧 Configurações

### Conexão com Banco de Dados
O sistema está configurado para conectar ao banco IBM DB2 com as seguintes configurações:
- **Host:** 10.64.1.11
- **Porta:** 50000
- **Database:** SAB
- **Usuário:** db2user_ro (somente leitura)

### Parâmetros de Análise
- **Período de análise:** 21 dias (configurável de 7 a 90 dias)
- **Período de projeção:** 15 dias (configurável de 1 a 60 dias)
- **Unidade de medida:** Unidades (un)

## 📋 Estrutura dos Dados

### Tabelas Utilizadas
- **DBA.ESTOQUE_ANALITICO** - Movimentações de estoque e vendas
- **DBA.PRODUTOS_VIEW** - Informações dos produtos
- **DBA.ESTOQUE_SALDO_ATUAL** - Saldo atual de estoque

### Métricas Calculadas (por Subgrupo)
- **Quantidade Vendida** - Vendas dos últimos N dias em unidades (soma de todos os produtos do subgrupo)
- **Estoque Atual** - Saldo atual em estoque em unidades (soma de todos os produtos do subgrupo)
- **Venda Diária Média** - Média de vendas por dia do subgrupo em unidades
- **Projeção de Venda** - Projeção para próximos N dias do subgrupo em unidades
- **Compra Recomendada** - Quantidade sugerida para compra do subgrupo em unidades
- **Dias de Estoque** - Quantos dias o estoque atual durará
- **Status do Estoque** - Classificação automática (Crítico/Baixo/Adequado/Alto)
- **Quantidade de Produtos** - Número de produtos diferentes no subgrupo

## 🎯 Como Usar

1. Execute `streamlit run dashboard.py`
2. Configure o período no painel lateral
3. Clique em "Gerar Análise Completa"
4. Visualize:
   - **Análise Geral**: Vendas e compras por subgrupo
   - **Análise por Loja**: Dados separados por loja
5. Exporte os dados em CSV se necessário

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

- Conexão com banco em **modo somente leitura**
- **Cache de dados** por 5 minutos para performance
- **Tratamento de erros** robusto
- **Logs de conexão** para monitoramento

## 📈 Performance

- **Cache automático** de consultas (5 minutos)
- **Processamento otimizado** com Pandas
- **Visualizações responsivas** com Plotly
- **Filtros em tempo real** sem recarregar dados

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique se o driver ODBC está instalado
2. Confirme o acesso ao banco de dados
3. Execute `pip install -r requirements.txt` para atualizar dependências
4. Consulte os logs de erro no console

## 📝 Changelog

### v2.0.0 (Atual)
- ✅ Dashboard profissional com Streamlit
- ✅ Insights automáticos e alertas
- ✅ Exportação para Excel e CSV
- ✅ Visualizações interativas
- ✅ Filtros avançados
- ✅ Relatórios executivos

### v1.0.0
- ✅ Aplicação desktop com Tkinter
- ✅ Conexão com banco DB2
- ✅ Análise básica de vendas
- ✅ Sugestões de compra

---

**Desenvolvido para otimizar a gestão de compras e estoque de produtos essenciais.**