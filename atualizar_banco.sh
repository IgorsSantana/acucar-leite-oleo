#!/bin/bash

echo "============================================================"
echo "    ATUALIZADOR LOCAL - BANCO DE DADOS"
echo "============================================================"
echo
echo "Este script atualiza o banco interno que será usado"
echo "pelo dashboard público no Streamlit Cloud."
echo

menu() {
    echo
    echo "Opções:"
    echo "1. Atualizar com dados externos (DB2)"
    echo "2. Atualizar com dados simulados"
    echo "3. Verificar status atual"
    echo "4. Sair"
    echo
    
    read -p "Escolha uma opção (1-4): " opcao
    
    case $opcao in
        1)
            echo
            echo "Atualizando com dados externos..."
            python3 atualizar_banco_local.py externo
            echo
            echo "Para atualizar o Streamlit Cloud, execute:"
            echo "  git add dados_vendas.db"
            echo "  git commit -m 'Atualizar dados do banco externo'"
            echo "  git push origin main"
            read -p "Pressione Enter para continuar..."
            ;;
        2)
            echo
            echo "Atualizando com dados simulados..."
            python3 atualizar_banco_local.py simulado
            echo
            echo "Para atualizar o Streamlit Cloud, execute:"
            echo "  git add dados_vendas.db"
            echo "  git commit -m 'Atualizar dados simulados'"
            echo "  git push origin main"
            read -p "Pressione Enter para continuar..."
            ;;
        3)
            echo
            echo "Verificando status..."
            python3 atualizar_banco_local.py status
            read -p "Pressione Enter para continuar..."
            ;;
        4)
            echo
            echo "Até logo!"
            exit 0
            ;;
        *)
            echo "Opção inválida! Tente novamente."
            menu
            ;;
    esac
}

menu
