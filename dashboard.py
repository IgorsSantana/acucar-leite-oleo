import streamlit as st
import pyodbc
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurações do banco (com fallback para variáveis de ambiente)
try:
    from config import SUBGRUPOS_ALVO, CONFIG_CONEXAO
except ImportError:
    # Fallback para deploy
    SUBGRUPOS_ALVO = {
        211604: "ÓLEO",
        410204: "LEITE", 
        210604: "AÇÚCAR"
    }
    CONFIG_CONEXAO = {
        "DRIVER": "{IBM DB2 ODBC DRIVER}",
        "DATABASE": os.getenv("DB_NAME", "SAB"),
        "HOSTNAME": os.getenv("DB_HOST", "10.64.1.11"),
        "PORT": os.getenv("DB_PORT", "50000"),
        "PROTOCOL": "TCPIP",
        "UID": os.getenv("DB_USER", "db2user_ro"),
        "PWD": os.getenv("DB_PASSWORD", "Sup3rs44nt0")
    }

# --- Configuração da Página do Dashboard ---
st.set_page_config(
    page_title="📊 Análise Profissional de Vendas - Óleo, Açúcar e Leite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo CSS Personalizado ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
    .critical-alert {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-alert {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Configurações e Constantes ---
SUBGRUPOS_ALVO = {
    211604: "ÓLEO",
    410204: "LEITE", 
    210604: "AÇÚCAR"
}

CONFIG_CONEXAO = {
    "DRIVER": "{IBM DB2 ODBC DRIVER}",
    "DATABASE": "SAB",
    "HOSTNAME": "10.64.1.11",
    "PORT": "50000",
    "PROTOCOL": "TCPIP",
    "UID": "db2user_ro",
    "PWD": "Sup3rs4nt0"
}

# --- Funções de Análise Avançada ---
def calcular_metricas_avancadas(df):
    """Calcula métricas avançadas para análise profissional por subgrupo"""
    if df.empty:
        return {}
    
    metricas = {}
    
    # Métricas por subgrupo (já agrupados)
    for categoria in df['CATEGORIA'].unique():
        df_cat = df[df['CATEGORIA'] == categoria]
        if not df_cat.empty:
            metricas[categoria] = {
                'total_vendido': df_cat['QUANTIDADE_VENDIDA'].sum(),
                'total_estoque': df_cat['ESTOQUE_ATUAL'].sum(),
                'total_projecao': df_cat['PROJECAO_VENDA'].sum(),
                'total_comprar': df_cat['COMPRA_RECOMENDADA'].sum(),
                'lojas_com_estoque_baixo': len(df_cat[df_cat['STATUS_ESTOQUE'].isin(['Crítico', 'Baixo'])]),
                'lojas_sem_estoque': len(df_cat[df_cat['ESTOQUE_ATUAL'] == 0]),
                'lojas_sobre_estoque': len(df_cat[df_cat['STATUS_ESTOQUE'] == 'Alto']),
                'total_lojas': len(df_cat),
                'total_produtos_diferentes': df_cat['QTD_PRODUTOS'].sum()
            }
    
    # Métricas gerais
    metricas['geral'] = {
        'total_subgrupos': len(df),
        'lojas_ativas': df['ID_LOJA'].nunique(),
        'categorias_analisadas': df['CATEGORIA'].nunique(),
        'subgrupos_criticos': len(df[df['STATUS_ESTOQUE'] == 'Crítico']),
        'valor_total_projecao': df['PROJECAO_VENDA'].sum(),
        'valor_total_compras': df['COMPRA_RECOMENDADA'].sum(),
        'indice_rotatividade': df['QUANTIDADE_VENDIDA'].sum() / df['ESTOQUE_ATUAL'].sum() if df['ESTOQUE_ATUAL'].sum() > 0 else 0
    }
    
    return metricas

def gerar_insights_automaticos(metricas, df):
    """Gera insights automáticos baseados nos dados agrupados por subgrupo"""
    insights = []
    
    # Análise de estoque crítico por subgrupo
    subgrupos_criticos = df[df['STATUS_ESTOQUE'] == 'Crítico']
    if not subgrupos_criticos.empty:
        insights.append({
            'tipo': 'critical',
            'titulo': '⚠️ Atenção: Subgrupos com Necessidade Crítica de Compra',
            'descricao': f'{len(subgrupos_criticos)} subgrupos precisam de compra urgente. Verifique a lista de prioridades.',
            'dados': subgrupos_criticos[['CATEGORIA', 'ID_LOJA', 'COMPRA_RECOMENDADA', 'ESTOQUE_ATUAL', 'DIAS_ESTOQUE']].head(10)
        })
    
    # Análise de sobre-estoque por subgrupo
    subgrupos_sobre_estoque = df[df['STATUS_ESTOQUE'] == 'Alto']
    if not subgrupos_sobre_estoque.empty:
        insights.append({
            'tipo': 'warning',
            'titulo': '📦 Subgrupos com Excesso de Estoque',
            'descricao': f'{len(subgrupos_sobre_estoque)} subgrupos têm estoque excessivo. Considere promoções.',
            'dados': subgrupos_sobre_estoque[['CATEGORIA', 'ID_LOJA', 'ESTOQUE_ATUAL', 'PROJECAO_VENDA', 'DIAS_ESTOQUE']].head(10)
        })
    
    # Análise de performance por categoria
    for categoria, dados in metricas.items():
        if categoria != 'geral':
            if dados['lojas_com_estoque_baixo'] > 0:
                insights.append({
                    'tipo': 'info',
                    'titulo': f'📊 {categoria}: Situação do Estoque',
                    'descricao': f'{dados["lojas_com_estoque_baixo"]} lojas com estoque baixo/crítico, {dados["lojas_sem_estoque"]} sem estoque, {dados["lojas_sobre_estoque"]} com excesso.',
                    'dados': None
                })
    
    # Análise de produtos por subgrupo
    produtos_por_subgrupo = df.groupby('CATEGORIA')['QTD_PRODUTOS'].sum()
    for categoria, qtd_produtos in produtos_por_subgrupo.items():
        if qtd_produtos > 0:
            insights.append({
                'tipo': 'success',
                'titulo': f'📦 {categoria}: Diversificação de Produtos',
                'descricao': f'{qtd_produtos} produtos diferentes disponíveis nesta categoria.',
                'dados': None
            })
    
    return insights

# --- Função para Dados de Demonstração ---
def gerar_dados_demo(dias_analise, dias_projecao):
    """Gera dados simulados para demonstração em deploy."""
    
    # Dados simulados realistas
    dados_demo = []
    lojas = [1, 2, 3, 4, 5]
    
    for loja in lojas:
        for codigo, categoria in SUBGRUPOS_ALVO.items():
            # Vendas simuladas (variando por categoria)
            vendas_base = {
                "ÓLEO": 1500,
                "AÇÚCAR": 2200, 
                "LEITE": 1800
            }
            
            # Adicionar variação aleatória
            vendas = vendas_base[categoria] + np.random.randint(-300, 500)
            estoque = vendas + np.random.randint(-200, 300)
            
            # Cálculos
            venda_diaria = vendas / dias_analise
            projecao = venda_diaria * dias_projecao
            compra_recomendada = max(0, projecao - estoque)
            
            dados_demo.append({
                'ID_LOJA': loja,
                'CODIGO_SUBGRUPO': codigo,
                'CATEGORIA': categoria,
                'QUANTIDADE_VENDIDA': vendas,
                'ESTOQUE_ATUAL': estoque,
                'VENDA_DIARIA_MEDIA': venda_diaria,
                'PROJECAO_VENDA': projecao,
                'COMPRA_RECOMENDADA': compra_recomendada
            })
    
    return pd.DataFrame(dados_demo)

# --- Caching da Função de Busca de Dados ---
@st.cache_data(ttl=300)  # Cache por 5 minutos
def buscar_dados_relatorio(dias_analise, dias_projecao):
    """Conecta ao DB, executa a query e retorna um DataFrame com os dados."""
    
    # Verificar se está em ambiente de deploy (modo demonstração)
    if os.getenv("STREAMLIT_SHARING") or os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER"):
        st.warning("🚧 **Modo Demonstração** - Dados simulados para deploy")
        return gerar_dados_demo(dias_analise, dias_projecao)
    
    connection_string = (
        f"DRIVER={CONFIG_CONEXAO['DRIVER']};"
        f"DATABASE={CONFIG_CONEXAO['DATABASE']};"
        f"HOSTNAME={CONFIG_CONEXAO['HOSTNAME']};"
        f"PORT={CONFIG_CONEXAO['PORT']};"
        f"PROTOCOL={CONFIG_CONEXAO['PROTOCOL']};"
        f"UID={CONFIG_CONEXAO['UID']};"
        f"PWD={CONFIG_CONEXAO['PWD']};"
    )

    try:
        cnxn = pyodbc.connect(connection_string)
        
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias_analise)
        
        placeholders = ','.join(['?'] * len(SUBGRUPOS_ALVO))
        params = list(SUBGRUPOS_ALVO.keys()) + [data_inicio, data_fim]

        query = f"""
        WITH VendasAgregadas AS (
            SELECT
                VENDAS.IDEMPRESA, VENDAS.IDSUBPRODUTO, SUM(VENDAS.QTDPRODUTO) AS QUANTIDADE_VENDIDA
            FROM DBA.ESTOQUE_ANALITICO AS VENDAS
            INNER JOIN DBA.PRODUTOS_VIEW AS PROD ON VENDAS.IDSUBPRODUTO = PROD.IDSUBPRODUTO
            WHERE PROD.IDSUBGRUPO IN ({placeholders})
              AND VENDAS.TIPOCATEGORIA = 'A' AND VENDAS.FLAGMOVSALDOPRO = 'T'
              AND VENDAS.DTMOVIMENTO BETWEEN ? AND ?
            GROUP BY VENDAS.IDEMPRESA, VENDAS.IDSUBPRODUTO
        )
        SELECT
            V.IDEMPRESA AS ID_LOJA, P.IDSUBGRUPO AS CODIGO_SUBGRUPO, V.IDSUBPRODUTO AS CODIGO_PRODUTO,
            P.DESCRICAOPRODUTO AS DESCRICAO_PRODUTO, V.QUANTIDADE_VENDIDA,
            COALESCE(E.QTDATUALESTOQUE, 0) AS ESTOQUE_ATUAL
        FROM VendasAgregadas AS V
        INNER JOIN DBA.PRODUTOS_VIEW AS P ON V.IDSUBPRODUTO = P.IDSUBPRODUTO
        LEFT JOIN DBA.ESTOQUE_SALDO_ATUAL AS E ON V.IDSUBPRODUTO = E.IDSUBPRODUTO AND V.IDEMPRESA = E.IDEMPRESA AND E.IDLOCALESTOQUE = 1
        """
        
        df = pd.read_sql(query, cnxn, params=params)
        cnxn.close()

        if df.empty:
            return pd.DataFrame()

        # Conversão de unidades (dividir por 1000, mantendo unidade como "unidades")
        df['QUANTIDADE_VENDIDA'] = df['QUANTIDADE_VENDIDA'] / 1000
        df['ESTOQUE_ATUAL'] = df['ESTOQUE_ATUAL'] / 1000
        
        # Adicionar categoria para facilitar análise
        df['CATEGORIA'] = df['CODIGO_SUBGRUPO'].map(SUBGRUPOS_ALVO)
        
        # AGRUPAR POR SUBGRUPO E LOJA - Esta é a mudança principal
        df_agrupado = df.groupby(['ID_LOJA', 'CODIGO_SUBGRUPO', 'CATEGORIA']).agg({
            'QUANTIDADE_VENDIDA': 'sum',
            'ESTOQUE_ATUAL': 'sum',
            'DESCRICAO_PRODUTO': 'count'  # Contar quantos produtos diferentes
        }).reset_index()
        
        # Renomear coluna de contagem
        df_agrupado.rename(columns={'DESCRICAO_PRODUTO': 'QTD_PRODUTOS'}, inplace=True)
        
        # Cálculos de projeção por subgrupo
        df_agrupado['VENDA_DIARIA_MEDIA'] = df_agrupado['QUANTIDADE_VENDIDA'] / dias_analise
        df_agrupado['PROJECAO_VENDA'] = df_agrupado['VENDA_DIARIA_MEDIA'] * dias_projecao
        df_agrupado['COMPRA_RECOMENDADA'] = (df_agrupado['PROJECAO_VENDA'] - df_agrupado['ESTOQUE_ATUAL']).clip(lower=0)
        
        # Calcular dias de estoque por subgrupo
        df_agrupado['DIAS_ESTOQUE'] = np.where(df_agrupado['VENDA_DIARIA_MEDIA'] > 0, 
                                              df_agrupado['ESTOQUE_ATUAL'] / df_agrupado['VENDA_DIARIA_MEDIA'], 
                                              np.inf)
        
        # Status do estoque por subgrupo
        df_agrupado['STATUS_ESTOQUE'] = pd.cut(df_agrupado['DIAS_ESTOQUE'], 
                                              bins=[0, 3, 7, 15, np.inf], 
                                              labels=['Crítico', 'Baixo', 'Adequado', 'Alto'])
        
        return df_agrupado

    except Exception as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
        return pd.DataFrame()


# --- Interface Principal do Dashboard ---

# Header principal
st.markdown('<h1 class="main-header">📊 Análise de Vendas e Compras</h1>', unsafe_allow_html=True)
st.markdown("**Óleo, Açúcar e Leite - Análise Simplificada por Subgrupo**")
st.markdown("---")

# Sidebar com controles
with st.sidebar:
    st.markdown("### ⚙️ Configurações de Análise")
    
    dias_analise = st.number_input(
        "📅 Período de Análise (dias)", 
        min_value=7, max_value=90, value=21, step=7,
        help="Quantos dias de vendas usar para calcular a média"
    )
    
    dias_projecao = st.number_input(
        "🎯 Projeção de Compra (dias)", 
        min_value=1, max_value=60, value=15, step=1,
        help="Para quantos dias projetar a necessidade de compra"
    )
    
    st.markdown("---")
    
    if st.button("🚀 Gerar Análise Completa", type="primary", use_container_width=True):
        with st.spinner("🔄 Conectando ao banco e processando dados..."):
            st.session_state.df_dados = buscar_dados_relatorio(dias_analise, dias_projecao)
            if not st.session_state.df_dados.empty:
                st.session_state.metricas = calcular_metricas_avancadas(st.session_state.df_dados)
                st.session_state.insights = gerar_insights_automaticos(st.session_state.metricas, st.session_state.df_dados)
                st.success("✅ Dados carregados com sucesso!")
    
    # Filtros simples
    if 'df_dados' in st.session_state and not st.session_state.df_dados.empty:
        st.markdown("### 🔍 Filtros")
        
        lista_lojas = ["Todas as Lojas"] + sorted(st.session_state.df_dados['ID_LOJA'].unique().tolist())
        loja_selecionada = st.selectbox("🏪 Selecionar Loja", options=lista_lojas)

# Verificação se há dados para exibir
if 'df_dados' in st.session_state and not st.session_state.df_dados.empty:
    df_filtrado = st.session_state.df_dados.copy()
    
    # Aplicar filtro de loja
    if 'loja_selecionada' in locals() and loja_selecionada != "Todas as Lojas":
        df_filtrado = df_filtrado[df_filtrado['ID_LOJA'] == loja_selecionada]

    # === SEÇÃO 1: ANÁLISE GERAL POR SUBGRUPO ===
    st.markdown("## 📊 Análise Geral por Subgrupo")
    
    # Resumo geral por categoria
    resumo_geral = df_filtrado.groupby('CATEGORIA').agg({
        'QUANTIDADE_VENDIDA': 'sum',
        'COMPRA_RECOMENDADA': 'sum'
    }).round(0).astype(int)
    
    resumo_geral.columns = ['Vendas (un)', 'Comprar (un)']
    resumo_geral.index.name = 'Subgrupo'
    
    # Formatar os dados (usando ponto como separador de milhares)
    resumo_geral_formatado = resumo_geral.style.format({
        'Vendas (un)': lambda x: f"{x:,.0f}".replace(',', '.'),
        'Comprar (un)': lambda x: f"{x:,.0f}".replace(',', '.')
    })
    
    st.dataframe(resumo_geral_formatado, use_container_width=True)
    
    # Gráfico simples
    col1, col2 = st.columns(2)
    
    with col1:
        fig_vendas = px.bar(
            x=resumo_geral.index,
            y=resumo_geral['Vendas (un)'],
            title="💰 Vendas por Subgrupo (unidades)",
            color=resumo_geral['Vendas (un)'],
            color_continuous_scale='Blues'
        )
        fig_vendas.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        fig_compras = px.bar(
            x=resumo_geral.index,
            y=resumo_geral['Comprar (un)'],
            title="🛒 Compras Recomendadas por Subgrupo (unidades)",
            color=resumo_geral['Comprar (un)'],
            color_continuous_scale='Reds'
        )
        fig_compras.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_compras, use_container_width=True)

    # === SEÇÃO 2: ANÁLISE POR LOJA ===
    st.markdown("## 🏪 Análise por Loja")
    
    # Dados por loja
    dados_por_loja = df_filtrado.groupby(['ID_LOJA', 'CATEGORIA']).agg({
        'QUANTIDADE_VENDIDA': 'sum',
        'COMPRA_RECOMENDADA': 'sum'
    }).round(0).astype(int)
    
    # Pivotar para melhor visualização
    vendas_por_loja = dados_por_loja['QUANTIDADE_VENDIDA'].unstack(fill_value=0)
    compras_por_loja = dados_por_loja['COMPRA_RECOMENDADA'].unstack(fill_value=0)
    
    st.markdown("### 💰 Vendas por Loja e Subgrupo (unidades)")
    st.dataframe(
        vendas_por_loja.style.format(lambda x: f"{x:,.0f}".replace(',', '.')),
        use_container_width=True
    )
    
    st.markdown("### 🛒 Compras Recomendadas por Loja e Subgrupo (unidades)")
    st.dataframe(
        compras_por_loja.style.format(lambda x: f"{x:,.0f}".replace(',', '.')),
        use_container_width=True
    )
    
    # === SEÇÃO 3: EXPORTAÇÃO SIMPLES ===
    st.markdown("## 📁 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Exportar resumo geral
        csv_geral = resumo_geral.to_csv()
        st.download_button(
            label="📄 Baixar Resumo Geral (CSV)",
            data=csv_geral,
            file_name=f"resumo_geral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Exportar dados por loja
        csv_loja = dados_por_loja.to_csv()
        st.download_button(
            label="📄 Baixar Dados por Loja (CSV)",
            data=csv_loja,
            file_name=f"dados_por_loja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )


else:
    # Tela inicial quando não há dados
    st.markdown("## 🚀 Sistema de Análise Simplificada")
    
    st.markdown("""
    ### 📊 O que este sistema mostra:
    
    **1. Análise Geral por Subgrupo:**
    - Vendas de cada categoria (Óleo, Açúcar, Leite) em unidades
    - Compras recomendadas para cada categoria em unidades
    
    **2. Análise por Loja:**
    - Vendas de cada categoria por loja em unidades
    - Compras recomendadas por loja e categoria em unidades
    
    ### 🎯 Produtos analisados:
    - **Óleo** (Subgrupo 211604)
    - **Açúcar** (Subgrupo 210604) 
    - **Leite** (Subgrupo 410204)
    
    ### 💡 Como usar:
    1. Configure o período no painel lateral
    2. Clique em "Gerar Análise Completa"
    3. Visualize vendas e compras por subgrupo
    4. Exporte os dados se necessário
    """)
    
    st.info("👈 **Configure os parâmetros no painel à esquerda e clique em 'Gerar Análise Completa' para começar!**")