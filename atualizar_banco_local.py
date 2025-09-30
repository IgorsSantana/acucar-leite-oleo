#!/usr/bin/env python3
"""
Script para Atualização Local do Banco de Dados
Execute este script no seu computador para atualizar o banco interno
que será usado pelo dashboard público no Streamlit Cloud.
"""

import sys
import os
from datetime import datetime
from database_manager import DatabaseManager

def atualizar_banco_externo():
    """Atualiza o banco com dados externos do DB2"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando atualização com dados externos...")
    
    try:
        db = DatabaseManager()
        registros = db.atualizar_dados(usar_dados_externos=True, dias_analise=21, dias_projecao=15)
        
        if registros > 0:
            print(f"✅ Sucesso! {registros} registros atualizados do banco externo")
            
            # Salvar log
            with open("log_atualizacao.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} - Dados externos: {registros} registros\n")
            
            print("📤 Agora faça commit e push para atualizar o Streamlit Cloud:")
            print("   git add dados_vendas.db")
            print("   git commit -m 'Atualizar dados do banco externo'")
            print("   git push origin main")
            
            return True
        else:
            print("❌ Nenhum registro foi atualizado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na atualização: {e}")
        with open("log_erros.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - ERRO: {e}\n")
        return False

def atualizar_banco_simulado():
    """Função removida - apenas dados reais são permitidos"""
    print("❌ Dados simulados não são permitidos neste sistema!")
    print("✅ Use apenas dados reais do banco externo.")
    return False

def verificar_status():
    """Verifica o status atual do banco"""
    print("📊 Verificando status do banco...")
    
    try:
        db = DatabaseManager()
        df = db.buscar_dados_dashboard()
        
        if df.empty:
            print("⚠️ Banco vazio!")
            return False
        
        print(f"✅ {len(df)} registros encontrados")
        
        # Resumo por categoria
        if 'CATEGORIA' in df.columns:
            resumo = df.groupby('CATEGORIA').agg({
                'QUANTIDADE_VENDIDA': 'sum',
                'COMPRA_RECOMENDADA': 'sum'
            }).round(0).astype(int)
            print("\n📋 Resumo por categoria:")
            print(resumo)
        
        # Configurações
        configs = db.obter_configuracoes()
        ultima_atualizacao = configs.get('ultima_atualizacao', {}).get('valor', 'N/A')
        fonte_dados = configs.get('fonte_dados', {}).get('valor', 'simulados')
        
        print(f"\n📅 Última atualização: {ultima_atualizacao}")
        print(f"🔗 Fonte dos dados: {fonte_dados}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🗄️  ATUALIZADOR LOCAL - BANCO DE DADOS")
    print("=" * 60)
    print()
    print("Este script atualiza o banco interno que será usado")
    print("pelo dashboard público no Streamlit Cloud.")
    print()
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "externo":
            atualizar_banco_externo()
        elif comando == "status":
            verificar_status()
        else:
            print("❌ Comando inválido!")
            print("Comandos disponíveis: externo, status")
    else:
        # Menu interativo
        print("📋 Opções:")
        print("1. Atualizar com dados externos (DB2)")
        print("2. Verificar status atual")
        print("3. Sair")
        print()
        
        while True:
            try:
                opcao = input("Escolha uma opção (1-3): ").strip()
                
                if opcao == "1":
                    if atualizar_banco_externo():
                        print("\n🎉 Atualização concluída! Faça commit e push para atualizar o Streamlit Cloud.")
                    break
                elif opcao == "2":
                    verificar_status()
                    break
                elif opcao == "3":
                    print("👋 Até logo!")
                    break
                else:
                    print("❌ Opção inválida! Escolha 1-3.")
                    
            except KeyboardInterrupt:
                print("\n👋 Operação cancelada pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
