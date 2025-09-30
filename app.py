import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
import pandas as pd
from datetime import datetime, timedelta
import threading

# --- PARTE 1: LÓGICA DE DADOS ---
# Esta função contém toda a lógica de banco de dados que já criamos.
# Ela foi adaptada para RETORNAR os dados em vez de imprimir no console.

def buscar_dados_relatorio():
    """Conecta ao DB, executa a query e retorna um DataFrame com os dados ou None em caso de erro."""
    
    connection_string = (
        "DRIVER={IBM DB2 ODBC DRIVER};"
        "DATABASE=SAB;"
        "HOSTNAME=10.64.1.11;"
        "PORT=50000;"
        "PROTOCOL=TCPIP;"
        "UID=db2user_ro;"
        "PWD=Sup3rs4nt0;"
    )
    
    DIAS_ANALISE = 21
    DIAS_PROJECAO = 15
    SUBGRUPOS_ALVO = [211604, 410204, 210604]

    try:
        cnxn = pyodbc.connect(connection_string)
        
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=DIAS_ANALISE)
        
        placeholders = ','.join(['?'] * len(SUBGRUPOS_ALVO))
        params = SUBGRUPOS_ALVO + [data_inicio, data_fim]

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

        # Cálculos de projeção e recomendação
        df['QUANTIDADE_VENDIDA'] = df['QUANTIDADE_VENDIDA'] / 1000
        df['ESTOQUE_ATUAL'] = df['ESTOQUE_ATUAL'] / 1000
        df['PROJECAO_VENDA'] = (df['QUANTIDADE_VENDIDA'] / DIAS_ANALISE) * DIAS_PROJECAO
        df['COMPRA_RECOMENDADA'] = df['PROJECAO_VENDA'] - df['ESTOQUE_ATUAL']
        df['COMPRA_RECOMENDADA'] = df['COMPRA_RECOMENDADA'].clip(lower=0)
        
        return df

    except pyodbc.Error as ex:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ou executar a consulta.\n\nDetalhes: {ex}")
        return None
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro durante o processamento.\n\nDetalhes: {e}")
        return None

# --- PARTE 2: APLICAÇÃO DA INTERFACE GRÁFICA (GUI) ---

class AppRelatorio:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatório de Sugestão de Compras")
        self.root.geometry("1200x700")

        self.DESCRICAO_SUBGRUPOS = {211604: "ÓLEO", 410204: "LEITE", 210604: "AÇÚCAR"}

        # Frame para os botões e status
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(fill=tk.X)

        self.btn_gerar = ttk.Button(top_frame, text="Gerar Relatório", command=self.iniciar_busca_dados)
        self.btn_gerar.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(top_frame, text="Pronto para gerar o relatório.", padding="0 0 10 0")
        self.status_label.pack(side=tk.RIGHT)

        # Treeview para exibir os dados
        tree_frame = ttk.Frame(root, padding="10")
        tree_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(tree_frame, columns=("Vendido", "Estoque", "Projeção", "Comprar"), show="tree headings")
        
        self.tree.heading("#0", text="Item (Loja / Subgrupo / Produto)")
        self.tree.heading("Vendido", text="Vendido (21d)")
        self.tree.heading("Estoque", text="Estoque Atual")
        self.tree.heading("Projeção", text="Projeção (15d)")
        self.tree.heading("Comprar", text="Sugestão Compra")

        self.tree.column("#0", width=500)
        self.tree.column("Vendido", width=120, anchor=tk.E)
        self.tree.column("Estoque", width=120, anchor=tk.E)
        self.tree.column("Projeção", width=120, anchor=tk.E)
        self.tree.column("Comprar", width=120, anchor=tk.E)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(expand=True, fill=tk.BOTH)

    def iniciar_busca_dados(self):
        self.btn_gerar.config(state="disabled")
        self.status_label.config(text="Buscando dados no banco... Aguarde.")
        self.limpar_treeview()
        
        thread = threading.Thread(target=self.rodar_thread_busca)
        thread.start()

    def rodar_thread_busca(self):
        df = buscar_dados_relatorio()
        self.root.after(0, self.finalizar_busca_dados, df)

    def finalizar_busca_dados(self, df):
        self.btn_gerar.config(state="normal")
        if df is not None:
            if df.empty:
                self.status_label.config(text="Nenhum dado encontrado para o período.")
            else:
                self.popular_treeview(df)
                self.status_label.config(text=f"Relatório gerado com sucesso! {len(df)} produtos analisados.")
        else:
            self.status_label.config(text="Ocorreu um erro ao buscar os dados.")

    def limpar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def popular_treeview(self, df):
        for id_loja, df_loja in df.groupby('ID_LOJA'):
            loja_id = f"loja_{id_loja}"
            self.tree.insert("", tk.END, iid=loja_id, text=f"LOJA: {id_loja}", open=True, tags=('loja',))
            
            for codigo_subgrupo, df_subgrupo in df_loja.groupby('CODIGO_SUBGRUPO'):
                descricao = self.DESCRICAO_SUBGRUPOS.get(codigo_subgrupo, f"Subgrupo {codigo_subgrupo}")
                subgrupo_id = f"{loja_id}_sub_{codigo_subgrupo}"
                
                total_vendido = df_subgrupo['QUANTIDADE_VENDIDA'].sum()
                total_estoque = df_subgrupo['ESTOQUE_ATUAL'].sum()
                total_projecao = df_subgrupo['PROJECAO_VENDA'].sum()
                total_comprar = df_subgrupo['COMPRA_RECOMENDADA'].sum()
                
                # MUDANÇA 1: Formatação do estoque do subgrupo para inteiro
                self.tree.insert(loja_id, tk.END, iid=subgrupo_id, text=f"{descricao} ({codigo_subgrupo})", open=True, tags=('subgrupo',),
                                 values=[f"{total_vendido:,.0f}", f"{int(total_estoque):,}", f"{total_projecao:,.0f}", f"{total_comprar:,.0f}"])
                
                for _, produto in df_subgrupo.iterrows():
                    produto_id = f"{subgrupo_id}_prod_{produto['CODIGO_PRODUTO']}"
                    item_text = f"  [{produto['CODIGO_PRODUTO']}] {produto['DESCRICAO_PRODUTO']}"
                    
                    # MUDANÇA 2: Formatação do estoque do produto para inteiro
                    self.tree.insert(subgrupo_id, tk.END, iid=produto_id, text=item_text,
                                     values=[f"{produto['QUANTIDADE_VENDIDA']:,.0f}", f"{int(produto['ESTOQUE_ATUAL']):,}",
                                             f"{produto['PROJECAO_VENDA']:,.0f}", f"{produto['COMPRA_RECOMENDADA']:,.0f}"])
        
        self.tree.tag_configure('loja', font=('Calibri', 12, 'bold'))
        self.tree.tag_configure('subgrupo', font=('Calibri', 11, 'italic'))

# --- PARTE 3: INICIALIZAÇÃO DA APLICAÇÃO ---

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRelatorio(root)
    root.mainloop()