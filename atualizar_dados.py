#!/usr/bin/env python3
"""
Script de Atualização Automática de Dados
Atualiza o banco interno SQLite com dados externos ou simulados
"""

import sys
import os
from datetime import datetime
from database_manager import DatabaseManager

def atualizar_dados_automatico():
    """Atualiza dados automaticamente"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando atualização automática...")
    
    try:
        db = DatabaseManager()
        
        # Tentar dados externos primeiro, fallback para simulados
        print("🌐 Tentando buscar dados externos...")
        registros = db.atualizar_dados(usar_dados_externos=True)
        
        if registros > 0:
            print(f"Atualização concluída: {registros} registros")
            
            # Salvar log
            with open("log_atualizacao.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} - Atualização automática: {registros} registros\n")
        else:
            print("Falha na atualização")
            
    except Exception as e:
        print(f"Erro na atualização: {e}")
        with open("log_erros.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - ERRO: {e}\n")

def atualizar_dados_simulados():
    """Atualiza com dados simulados"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Atualizando com dados simulados...")
    
    try:
        db = DatabaseManager()
        registros = db.atualizar_dados(usar_dados_externos=False)
        print(f"Dados simulados atualizados: {registros} registros")
        
        with open("log_atualizacao.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - Dados simulados: {registros} registros\n")
            
    except Exception as e:
        print(f"Erro na atualização simulada: {e}")

def verificar_dados():
    """Verifica dados atuais"""
    print("Verificando dados atuais...")
    
    try:
        db = DatabaseManager()
        df = db.buscar_dados_dashboard()
        
        if df.empty:
            print("⚠️ Banco vazio!")
            return False
        
        print(f"{len(df)} registros encontrados")
        print("Resumo por categoria:")
        if 'categoria' in df.columns:
            resumo = df.groupby('categoria').agg({
                'QUANTIDADE_VENDIDA': 'sum',
                'COMPRA_RECOMENDADA': 'sum'
            }).round(0).astype(int)
            print(resumo)
        else:
            print("Coluna CATEGORIA não encontrada")
            print("Colunas disponíveis:", list(df.columns))
        
        print(f"Última atualização: {db.obter_configuracoes().get('ultima_atualizacao', {}).get('valor', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao verificar dados: {e}")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "externo":
            atualizar_dados_automatico()
        elif comando == "simulado":
            atualizar_dados_simulados()
        elif comando == "verificar":
            verificar_dados()
        else:
            print("Comando inválido!")
            print("Comandos disponíveis: externo, simulado, verificar")
    else:
        # Menu interativo
        print("=" * 50)
        print("ATUALIZADOR DE DADOS - DASHBOARD VENDAS")
        print("=" * 50)
        print()
        print("Opções:")
        print("1. Atualizar com dados externos (DB2)")
        print("2. Atualizar com dados simulados")
        print("3. Verificar dados atuais")
        print("4. Sair")
        print()
        
        while True:
            try:
                opcao = input("Escolha uma opção (1-4): ").strip()
                
                if opcao == "1":
                    atualizar_dados_automatico()
                    break
                elif opcao == "2":
                    atualizar_dados_simulados()
                    break
                elif opcao == "3":
                    verificar_dados()
                    break
                elif opcao == "4":
                    print("Até logo!")
                    break
                else:
                    print("Opção inválida! Escolha 1-4.")
                    
            except KeyboardInterrupt:
                print("Operação cancelada pelo usuário.")
                break
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == "__main__":
    main()
