#!/bin/bash

echo "========================================"
echo "   AGENDADOR DE ATUALIZAÇÃO AUTOMÁTICA"
echo "========================================"
echo

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ ERRO: Python não está instalado"
        echo "Instale o Python em: https://python.org/downloads"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python encontrado: $PYTHON_CMD"

# Obter diretório atual
CURRENT_DIR=$(pwd)
SCRIPT_PATH="$CURRENT_DIR/atualizar_dados.py"

echo
echo "🔧 Configurando atualização automática..."
echo

# Criar script para cron
CRON_SCRIPT="$CURRENT_DIR/cron_atualizacao.sh"
cat > "$CRON_SCRIPT" << EOF
#!/bin/bash
cd "$CURRENT_DIR"
$PYTHON_CMD atualizar_dados.py externo >> log_cron.txt 2>&1
EOF

chmod +x "$CRON_SCRIPT"

# Adicionar ao crontab (executar a cada 4 horas)
CRON_JOB="0 */4 * * * $CRON_SCRIPT"

# Verificar se já existe
if crontab -l 2>/dev/null | grep -q "atualizar_dados.py"; then
    echo "⚠️  Já existe uma tarefa agendada"
    echo "📋 Tarefas atuais:"
    crontab -l | grep "atualizar_dados.py"
else
    # Adicionar nova tarefa
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Tarefa agendada criada com sucesso!"
    echo "📅 Atualização automática a cada 4 horas"
fi

echo
echo "🚀 Executando primeira atualização..."
$PYTHON_CMD atualizar_dados.py externo

echo
echo "========================================"
echo "✅ CONFIGURAÇÃO CONCLUÍDA!"
echo "========================================"
echo
echo "📋 O que foi configurado:"
echo "- ✅ Atualização automática a cada 4 horas"
echo "- ✅ Primeira atualização executada"
echo "- ✅ Banco de dados interno criado"
echo
echo "🎯 Para usar o dashboard:"
echo "1. Execute: streamlit run dashboard.py"
echo "2. Ou use o deploy no Streamlit Cloud"
echo
echo "📊 Para atualizar manualmente:"
echo "- $PYTHON_CMD atualizar_dados.py externo"
echo "- $PYTHON_CMD atualizar_dados.py simulado"
echo "- $PYTHON_CMD atualizar_dados.py verificar"
echo
echo "📋 Para ver tarefas agendadas:"
echo "- crontab -l"
echo
echo "🗑️  Para remover tarefa:"
echo "- crontab -e (edite e remova a linha)"
echo
