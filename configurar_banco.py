#!/usr/bin/env python3
"""
Configurador de Banco de Dados
Script para configurar as credenciais corretas do banco DB2
"""

import os
import getpass

def configurar_banco():
    """Configura as credenciais do banco DB2"""
    print("=" * 60)
    print("🔧 CONFIGURADOR DE BANCO DE DADOS")
    print("=" * 60)
    print()
    print("Configure as credenciais do banco DB2:")
    print()
    
    # Configurações atuais
    print("📋 Configurações atuais:")
    print("   Host: 10.64.1.11")
    print("   Porta: 50000")
    print("   Database: SAB")
    print("   Driver: IBM DB2 ODBC DRIVER")
    print()
    
    # Obter novas credenciais
    print("🔐 Digite as credenciais corretas:")
    usuario = input("👤 Usuário: ").strip()
    
    if not usuario:
        print("❌ Usuário não pode estar vazio!")
        return False
    
    senha = getpass.getpass("🔒 Senha: ")
    
    if not senha:
        print("❌ Senha não pode estar vazia!")
        return False
    
    # Confirmar senha
    senha_confirmar = getpass.getpass("🔒 Confirmar senha: ")
    
    if senha != senha_confirmar:
        print("❌ Senhas não coincidem!")
        return False
    
    # Criar arquivo de configuração
    config_content = f'''"""
Configurações do Banco de Dados
Arquivo gerado automaticamente pelo configurador
"""

# Configurações do banco DB2
CONFIG_CONEXAO = {{
    "DRIVER": "{{IBM DB2 ODBC DRIVER}}",
    "DATABASE": "SAB",
    "HOSTNAME": "10.64.1.11",
    "PORT": "50000",
    "PROTOCOL": "TCPIP",
    "UID": "{usuario}",
    "PWD": "{senha}"
}}

# Subgrupos alvo
SUBGRUPOS_ALVO = {{
    211604: "ÓLEO",
    410204: "LEITE",
    210604: "AÇÚCAR"
}}
'''
    
    try:
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        print()
        print("✅ Configuração salva em config.py")
        print()
        print("🧪 Testando conexão...")
        
        # Testar conexão
        if testar_conexao(usuario, senha):
            print("✅ Conexão bem-sucedida!")
            print()
            print("🚀 Agora você pode executar:")
            print("   python atualizar_banco_local.py externo")
            return True
        else:
            print("❌ Falha na conexão!")
            print("   Verifique se as credenciais estão corretas")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False

def testar_conexao(usuario, senha):
    """Testa a conexão com o banco"""
    try:
        import pyodbc
        
        connection_string = (
            f"DRIVER={{IBM DB2 ODBC DRIVER}};"
            f"DATABASE=SAB;"
            f"HOSTNAME=10.64.1.11;"
            f"PORT=50000;"
            f"PROTOCOL=TCPIP;"
            f"UID={usuario};"
            f"PWD={senha};"
        )
        
        print("   🔗 Conectando ao banco...")
        cnxn = pyodbc.connect(connection_string, timeout=10)
        
        print("   📊 Testando consulta...")
        cursor = cnxn.cursor()
        cursor.execute("SELECT 1 FROM SYSIBM.SYSDUMMY1")
        result = cursor.fetchone()
        
        cnxn.close()
        
        if result:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("Este script irá configurar as credenciais do banco DB2.")
    print("Certifique-se de ter as credenciais corretas antes de continuar.")
    print()
    
    continuar = input("Deseja continuar? (s/n): ").lower().strip()
    
    if continuar in ['s', 'sim', 'y', 'yes']:
        if configurar_banco():
            print()
            print("🎉 Configuração concluída com sucesso!")
        else:
            print()
            print("❌ Configuração falhou. Tente novamente.")
    else:
        print("👋 Operação cancelada.")

if __name__ == "__main__":
    main()
