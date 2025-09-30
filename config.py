# -*- coding: utf-8 -*-
"""
Configurações do Sistema de Análise de Vendas
Óleo, Açúcar e Leite
"""

# === CONFIGURAÇÕES DE BANCO DE DADOS ===
DATABASE_CONFIG = {
    "DRIVER": "{IBM DB2 ODBC DRIVER}",
    "DATABASE": "SAB",
    "HOSTNAME": "10.64.1.11",
    "PORT": "50000",
    "PROTOCOL": "TCPIP",
    "UID": "db2user_ro",
    "PWD": "Sup3rs4nt0"
}

# === PRODUTOS ANALISADOS ===
SUBGRUPOS_ALVO = {
    211604: "ÓLEO",
    410204: "LEITE", 
    210604: "AÇÚCAR"
}

# === CONFIGURAÇÕES PADRÃO ===
DEFAULT_DAYS_ANALYSIS = 21  # Dias para análise de vendas
DEFAULT_DAYS_PROJECTION = 15  # Dias para projeção de compra
MIN_DAYS_ANALYSIS = 7
MAX_DAYS_ANALYSIS = 90
MIN_DAYS_PROJECTION = 1
MAX_DAYS_PROJECTION = 60

# === CONFIGURAÇÕES DE ESTOQUE ===
STOCK_STATUS_THRESHOLDS = {
    "CRITICAL": 3,    # Menos de 3 dias = Crítico
    "LOW": 7,         # Menos de 7 dias = Baixo
    "ADEQUATE": 15,   # Menos de 15 dias = Adequado
    "HIGH": float('inf')  # Mais de 15 dias = Alto
}

# === CONFIGURAÇÕES DE CACHE ===
CACHE_TTL_SECONDS = 300  # 5 minutos

# === CONFIGURAÇÕES DE EXPORTAÇÃO ===
EXPORT_FORMATS = {
    "EXCEL": "xlsx",
    "CSV": "csv"
}

# === MENSAGENS DO SISTEMA ===
MESSAGES = {
    "WELCOME": "Bem-vindo ao Sistema de Análise de Vendas",
    "LOADING": "Carregando dados...",
    "SUCCESS": "Dados carregados com sucesso!",
    "ERROR_DB": "Erro ao conectar ao banco de dados",
    "NO_DATA": "Nenhum dado encontrado para o período",
    "GENERATING_REPORT": "Gerando relatório..."
}

# === CONFIGURAÇÕES DE INTERFACE ===
UI_CONFIG = {
    "PAGE_TITLE": "📊 Análise Profissional de Vendas - Óleo, Açúcar e Leite",
    "PAGE_ICON": "📊",
    "LAYOUT": "wide",
    "SIDEBAR_STATE": "expanded"
}

# === CONFIGURAÇÕES DE VISUALIZAÇÃO ===
CHART_CONFIG = {
    "HEIGHT": 400,
    "COLOR_SCALE": "Blues",
    "CRITICAL_COLOR": "#ff4444",
    "LOW_COLOR": "#ffaa00",
    "ADEQUATE_COLOR": "#00aa44",
    "HIGH_COLOR": "#0066cc"
}
