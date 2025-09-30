#!/bin/bash

echo "========================================"
echo "   UPLOAD PARA GITHUB - DASHBOARD"
echo "========================================"
echo

# Verificar se git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ ERRO: Git não está instalado"
    echo "Instale com: sudo apt-get install git (Ubuntu/Debian)"
    echo "ou: brew install git (macOS)"
    exit 1
fi

echo "✅ Git encontrado!"

# Inicializar repositório se não existir
if [ ! -d ".git" ]; then
    echo
    echo "🔧 Inicializando repositório Git..."
    git init
    echo "✅ Repositório inicializado!"
fi

# Adicionar todos os arquivos
echo
echo "📁 Adicionando arquivos..."
git add .
echo "✅ Arquivos adicionados!"

# Fazer commit
echo
echo "💾 Fazendo commit..."
git commit -m "Dashboard de análise de vendas - Óleo, Açúcar e Leite

- Sistema completo de análise de vendas
- Dados simulados para demonstração
- Deploy pronto para Streamlit Cloud
- Formatação com ponto como separador
- Unidades em vez de quilogramas
- Cache otimizado para performance
- Interface responsiva e profissional"

echo "✅ Commit realizado!"

# Configurar remote
echo
echo "🌐 Configurando repositório remoto..."
echo
echo "Por favor, cole a URL do seu repositório GitHub:"
echo "Exemplo: https://github.com/seu-usuario/dashboard-vendas.git"
echo
read -p "URL do repositório: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ URL não fornecida. Execute novamente e forneça a URL."
    exit 1
fi

# Verificar se remote já existe
if git remote -v | grep -q "origin"; then
    echo "🔄 Atualizando remote origin..."
    git remote set-url origin "$REPO_URL"
else
    echo "🔗 Adicionando remote origin..."
    git remote add origin "$REPO_URL"
fi

echo "✅ Remote configurado!"

# Push para GitHub
echo
echo "🚀 Enviando para GitHub..."
git push -u origin main

if [ $? -ne 0 ]; then
    echo
    echo "⚠️  Tentando com branch 'master'..."
    git push -u origin master
fi

echo
echo "========================================"
echo "✅ UPLOAD CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo
echo "🌐 Seu repositório está disponível em:"
echo "$REPO_URL"
echo
echo "🚀 Para fazer deploy no Streamlit Cloud:"
echo "1. Acesse: https://share.streamlit.io/"
echo "2. Login com GitHub"
echo "3. New app → Selecione seu repositório"
echo "4. Main file: dashboard.py"
echo "5. Deploy!"
echo
