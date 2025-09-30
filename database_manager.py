"""
Gerenciador de Banco de Dados Interno
Sistema para criar e atualizar banco SQLite com dados de vendas
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configurações com fallback
try:
    from config import SUBGRUPOS_ALVO, CONFIG_CONEXAO
except ImportError:
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
        "PWD": "Sup3rs44nt0"
    }

try:
    import pyodbc
    PYODBC_DISPONIVEL = True
except ImportError:
    PYODBC_DISPONIVEL = False
    print("⚠️ pyodbc não disponível, apenas dados simulados")

class DatabaseManager:
    def __init__(self, db_path="dados_vendas.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda DATE,
                id_loja INTEGER,
                codigo_subgrupo INTEGER,
                categoria TEXT,
                quantidade_vendida REAL,
                estoque_atual REAL,
                venda_diaria_media REAL,
                projecao_venda REAL,
                compra_recomendada REAL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Criar tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INTEGER PRIMARY KEY,
                chave TEXT UNIQUE,
                valor TEXT,
                descricao TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inserir configurações padrão
        configuracoes_padrao = [
            ('dias_analise', '21', 'Período de análise em dias'),
            ('dias_projecao', '15', 'Período de projeção em dias'),
            ('ultima_atualizacao', datetime.now().isoformat(), 'Data da última atualização dos dados')
        ]
        
        for chave, valor, descricao in configuracoes_padrao:
            cursor.execute('''
                INSERT OR REPLACE INTO configuracoes (chave, valor, descricao)
                VALUES (?, ?, ?)
            ''', (chave, valor, descricao))
        
        conn.commit()
        conn.close()
        print(f"Banco de dados inicializado: {self.db_path}")
    
    def conectar_banco_externo(self):
        """Conecta ao banco externo DB2"""
        if not PYODBC_DISPONIVEL:
            return None
            
        try:
            connection_string = (
                f"DRIVER={CONFIG_CONEXAO['DRIVER']};"
                f"DATABASE={CONFIG_CONEXAO['DATABASE']};"
                f"HOSTNAME={CONFIG_CONEXAO['HOSTNAME']};"
                f"PORT={CONFIG_CONEXAO['PORT']};"
                f"PROTOCOL={CONFIG_CONEXAO['PROTOCOL']};"
                f"UID={CONFIG_CONEXAO['UID']};"
                f"PWD={CONFIG_CONEXAO['PWD']};"
            )
            cnxn = pyodbc.connect(connection_string)
            return cnxn
        except Exception as e:
            print(f"Erro ao conectar ao banco externo: {e}")
            return None
    
    def buscar_dados_externos(self, dias_analise=21):
        """Busca dados do banco externo"""
        cnxn = self.conectar_banco_externo()
        if not cnxn:
            return None
        
        try:
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
                V.IDEMPRESA AS ID_LOJA, P.IDSUBGRUPO AS CODIGO_SUBGRUPO, V.QUANTIDADE_VENDIDA,
                COALESCE(E.QTDATUALESTOQUE, 0) AS ESTOQUE_ATUAL
            FROM VendasAgregadas AS V
            INNER JOIN DBA.PRODUTOS_VIEW AS P ON V.IDSUBPRODUTO = P.IDSUBPRODUTO
            LEFT JOIN DBA.ESTOQUE_SALDO_ATUAL AS E ON V.IDSUBPRODUTO = E.IDSUBPRODUTO AND V.IDEMPRESA = E.IDEMPRESA AND E.IDLOCALESTOQUE = 1
            """
            
            df = pd.read_sql(query, cnxn, params=params)
            cnxn.close()
            
            if df.empty:
                return None
            
            # Conversão de unidades (dividir por 1000)
            df['QUANTIDADE_VENDIDA'] = df['QUANTIDADE_VENDIDA'] / 1000
            df['ESTOQUE_ATUAL'] = df['ESTOQUE_ATUAL'] / 1000
            
            # Adicionar categoria
            df['CATEGORIA'] = df['CODIGO_SUBGRUPO'].map(SUBGRUPOS_ALVO)
            
            # Agrupar por subgrupo e loja
            df_agrupado = df.groupby(['ID_LOJA', 'CODIGO_SUBGRUPO', 'CATEGORIA']).agg({
                'QUANTIDADE_VENDIDA': 'sum',
                'ESTOQUE_ATUAL': 'sum',
            }).reset_index()
            
            return df_agrupado
            
        except Exception as e:
            print(f"Erro ao buscar dados externos: {e}")
            if cnxn:
                cnxn.close()
            return None
    
    def gerar_dados_demo(self, dias_analise=21, dias_projecao=15):
        """Gera dados simulados para demonstração"""
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
                np.random.seed(loja + codigo)  # Para consistência
                vendas = vendas_base[categoria] + np.random.randint(-300, 500)
                estoque = vendas + np.random.randint(-200, 300)
                
                # Cálculos
                venda_diaria = vendas / dias_analise
                projecao = venda_diaria * dias_projecao
                compra_recomendada = max(0, projecao - estoque)
                
                dados_demo.append({
                    'data_venda': datetime.now().date(),
                    'id_loja': loja,
                    'codigo_subgrupo': codigo,
                    'categoria': categoria,
                    'quantidade_vendida': vendas,
                    'estoque_atual': estoque,
                    'venda_diaria_media': venda_diaria,
                    'projecao_venda': projecao,
                    'compra_recomendada': compra_recomendada
                })
        
        return pd.DataFrame(dados_demo)
    
    def atualizar_dados(self, usar_dados_externos=True, dias_analise=21, dias_projecao=15):
        """Atualiza os dados no banco interno"""
        print(f"Iniciando atualização dos dados...")
        
        # Limpar dados antigos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM vendas')
        
        # Buscar dados
        if usar_dados_externos:
            print("🌐 Tentando buscar dados do banco externo...")
            df = self.buscar_dados_externos(dias_analise)
            if df is None:
                print("⚠️ Falha na conexão externa, usando dados simulados")
                df = self.gerar_dados_demo(dias_analise, dias_projecao)
                fonte = "simulados"
            else:
                print("✅ Dados externos obtidos com sucesso!")
                # Calcular projeções
                df['venda_diaria_media'] = df['QUANTIDADE_VENDIDA'] / dias_analise
                df['projecao_venda'] = df['venda_diaria_media'] * dias_projecao
                df['compra_recomendada'] = (df['projecao_venda'] - df['ESTOQUE_ATUAL']).clip(lower=0)
                df['data_venda'] = datetime.now().date()
                df = df.rename(columns={
                    'ID_LOJA': 'id_loja',
                    'CODIGO_SUBGRUPO': 'codigo_subgrupo',
                    'QUANTIDADE_VENDIDA': 'quantidade_vendida',
                    'ESTOQUE_ATUAL': 'estoque_atual'
                })
                fonte = "externos"
        else:
            print("Usando dados simulados...")
            df = self.gerar_dados_demo(dias_analise, dias_projecao)
            fonte = "simulados"
        
        # Inserir dados no banco
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO vendas (
                    data_venda, id_loja, codigo_subgrupo, categoria,
                    quantidade_vendida, estoque_atual, venda_diaria_media,
                    projecao_venda, compra_recomendada
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['data_venda'], row['id_loja'], row['codigo_subgrupo'], row['categoria'],
                row['quantidade_vendida'], row['estoque_atual'], row['venda_diaria_media'],
                row['projecao_venda'], row['compra_recomendada']
            ))
        
        # Atualizar configurações
        cursor.execute('''
            UPDATE configuracoes SET valor = ? WHERE chave = 'ultima_atualizacao'
        ''', (datetime.now().isoformat(),))
        
        cursor.execute('''
            UPDATE configuracoes SET valor = ? WHERE chave = 'fonte_dados'
        ''', (fonte,))
        
        conn.commit()
        conn.close()
        
        print(f"Dados atualizados com sucesso! ({len(df)} registros)")
        print(f"Fonte dos dados: {fonte}")
        return len(df)
    
    def buscar_dados_dashboard(self, dias_analise=21, dias_projecao=15):
        """Busca dados formatados para o dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
        SELECT 
            id_loja, codigo_subgrupo, categoria,
            quantidade_vendida, estoque_atual, venda_diaria_media,
            projecao_venda, compra_recomendada
        FROM vendas
        ORDER BY id_loja, categoria
        '''
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        if df.empty:
            # Se não há dados, gerar dados demo
            print("Banco vazio, gerando dados demo...")
            self.atualizar_dados(usar_dados_externos=False, dias_analise=dias_analise, dias_projecao=dias_projecao)
            return self.buscar_dados_dashboard(dias_analise, dias_projecao)
        
        # Renomear colunas para compatibilidade
        df = df.rename(columns={
            'id_loja': 'ID_LOJA',
            'codigo_subgrupo': 'CODIGO_SUBGRUPO',
            'categoria': 'CATEGORIA',
            'quantidade_vendida': 'QUANTIDADE_VENDIDA',
            'estoque_atual': 'ESTOQUE_ATUAL',
            'venda_diaria_media': 'VENDA_DIARIA_MEDIA',
            'projecao_venda': 'PROJECAO_VENDA',
            'compra_recomendada': 'COMPRA_RECOMENDADA'
        })
        
        return df
    
    def obter_configuracoes(self):
        """Obtém configurações do banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT chave, valor, descricao FROM configuracoes')
        configs = {row[0]: {'valor': row[1], 'descricao': row[2]} for row in cursor.fetchall()}
        
        conn.close()
        return configs

# Função main removida - usar atualizar_dados.py
