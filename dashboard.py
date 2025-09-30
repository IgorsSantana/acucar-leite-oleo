import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta

# Configurações básicas
SUBGRUPOS_ALVO = {
    211604: "ÓLEO",
    410204: "LEITE", 
    210604: "AÇÚCAR"
}

# Importar o gerenciador de banco interno
try:
    from database_manager import DatabaseManager
    db_manager = DatabaseManager()
    BANCO_INTERNO_DISPONIVEL = True
except ImportError:
    BANCO_INTERNO_DISPONIVEL = False

# Configuração da página
st.set_page_config(
    page_title="📊 Análise de Vendas - Óleo, Açúcar e Leite",
    page_icon="📊",
    layout="wide"
)

# Função para gerar dados demo
def gerar_dados_demo(dias_analise, dias_projecao):
    """Gera dados simulados para demonstração"""
    dados_demo = []
    lojas = [1, 2, 3, 4, 5]
    
    for loja in lojas:
        for codigo, categoria in SUBGRUPOS_ALVO.items():
            vendas_base = {
                "ÓLEO": 1500,
                "AÇÚCAR": 2200, 
                "LEITE": 1800
            }
            
            np.random.seed(loja + codigo)
            vendas = vendas_base[categoria] + np.random.randint(-300, 500)
            estoque = vendas + np.random.randint(-200, 300)
            
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

@st.cache_data(ttl=300)
def buscar_dados_relatorio(dias_analise, dias_projecao):
    """Busca dados do banco interno ou gera dados simulados"""
    
    if BANCO_INTERNO_DISPONIVEL:
        try:
            df = db_manager.buscar_dados_dashboard(dias_analise, dias_projecao)
            if not df.empty:
                configs = db_manager.obter_configuracoes()
                ultima_atualizacao = configs.get('ultima_atualizacao', {}).get('valor', 'N/A')
                st.success(f"✅ **Dados do banco interno** - Última atualização: {ultima_atualizacao[:19]}")
                return df
        except Exception as e:
            st.warning(f"⚠️ Erro no banco interno: {e}")
    
    # Fallback para dados simulados
    if os.getenv("STREAMLIT_SHARING") or os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER"):
        st.warning("🚧 **Modo Demonstração** - Dados simulados para deploy")
    else:
        st.info("🎭 **Dados simulados** - Sistema offline")
    
    return gerar_dados_demo(dias_analise, dias_projecao)

# Interface principal
st.markdown('<h1 class="main-header">📊 Análise de Vendas e Compras</h1>', unsafe_allow_html=True)
st.markdown("**Óleo, Açúcar e Leite - Análise Simplificada por Subgrupo**")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configurações de Análise")
    
    dias_analise = st.number_input(
        "📅 Período de Análise (dias)", 
        min_value=7, max_value=90, value=21, step=7
    )
    
    dias_projecao = st.number_input(
        "🎯 Projeção de Compra (dias)", 
        min_value=1, max_value=60, value=15, step=1
    )
    
    st.markdown("---")
    
    if st.button("🚀 Gerar Análise Completa", type="primary", use_container_width=True):
        with st.spinner("🔄 Processando dados..."):
            st.session_state.df_dados = buscar_dados_relatorio(dias_analise, dias_projecao)
            if not st.session_state.df_dados.empty:
                st.success("✅ Dados carregados com sucesso!")
    
    # Botões de atualização (se banco interno disponível)
    if BANCO_INTERNO_DISPONIVEL:
        st.markdown("### 🔄 Atualização de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌐 Dados Externos", use_container_width=True):
                with st.spinner("🔄 Atualizando..."):
                    try:
                        registros = db_manager.atualizar_dados(usar_dados_externos=True, 
                                                              dias_analise=dias_analise, 
                                                              dias_projecao=dias_projecao)
                        st.success(f"✅ {registros} registros")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
        
        with col2:
            if st.button("🎭 Dados Simulados", use_container_width=True):
                with st.spinner("🔄 Gerando..."):
                    try:
                        registros = db_manager.atualizar_dados(usar_dados_externos=False, 
                                                              dias_analise=dias_analise, 
                                                              dias_projecao=dias_projecao)
                        st.success(f"✅ {registros} registros")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
    
    # Filtros
    if 'df_dados' in st.session_state and not st.session_state.df_dados.empty:
        st.markdown("### 🔍 Filtros")
        
        lista_lojas = ["Todas as Lojas"] + sorted(st.session_state.df_dados['ID_LOJA'].unique().tolist())
        loja_selecionada = st.selectbox("🏪 Selecionar Loja", options=lista_lojas)

# Exibição dos dados
if 'df_dados' in st.session_state and not st.session_state.df_dados.empty:
    df_filtrado = st.session_state.df_dados.copy()
    
    # Aplicar filtro de loja
    if 'loja_selecionada' in locals() and loja_selecionada != "Todas as Lojas":
        df_filtrado = df_filtrado[df_filtrado['ID_LOJA'] == loja_selecionada]

    # === ANÁLISE GERAL POR SUBGRUPO ===
    st.markdown("## 📊 Análise Geral por Subgrupo")
    
    # Resumo geral
    resumo_geral = df_filtrado.groupby('CATEGORIA').agg({
        'QUANTIDADE_VENDIDA': 'sum',
        'COMPRA_RECOMENDADA': 'sum'
    }).round(0).astype(int)
    
    resumo_geral.columns = ['Vendas (un)', 'Comprar (un)']
    resumo_geral.index.name = 'Subgrupo'
    
    # Formatação com ponto
    resumo_geral_formatado = resumo_geral.style.format({
        'Vendas (un)': lambda x: f"{x:,.0f}".replace(',', '.'),
        'Comprar (un)': lambda x: f"{x:,.0f}".replace(',', '.')
    })
    
    st.dataframe(resumo_geral_formatado, use_container_width=True)
    
    # Gráficos
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

    # === ANÁLISE POR LOJA ===
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
    
    # === EXPORTAÇÃO ===
    st.markdown("## 📁 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_geral = resumo_geral.to_csv()
        st.download_button(
            label="📄 Baixar Resumo Geral (CSV)",
            data=csv_geral,
            file_name=f"resumo_geral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        csv_loja = dados_por_loja.to_csv()
        st.download_button(
            label="📄 Baixar Dados por Loja (CSV)",
            data=csv_loja,
            file_name=f"dados_por_loja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # Tela inicial
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
