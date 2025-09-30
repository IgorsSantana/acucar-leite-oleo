@echo off
echo ========================================
echo   AGENDADOR DE ATUALIZACAO AUTOMATICA
echo ========================================
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado ou nao esta no PATH
    echo Instale o Python em: https://python.org/downloads
    pause
    exit /b 1
)

echo ✅ Python encontrado!

REM Criar tarefa agendada para atualização a cada 4 horas
echo.
echo 🔧 Configurando atualização automática...
echo.

REM Criar script temporário para o agendador
echo @echo off > temp_task.bat
echo cd /d "%~dp0" >> temp_task.bat
echo python atualizar_dados.py externo >> temp_task.bat

REM Criar tarefa no Windows Task Scheduler
schtasks /create /tn "DashboardVendas_Atualizacao" /tr "%~dp0temp_task.bat" /sc hourly /mo 4 /ru "SYSTEM" /f >nul 2>&1

if errorlevel 1 (
    echo ⚠️  Não foi possível criar tarefa agendada automaticamente.
    echo.
    echo 📋 Para agendar manualmente:
    echo 1. Abra o "Agendador de Tarefas" do Windows
    echo 2. Criar Tarefa Básica
    echo 3. Nome: "Dashboard Vendas - Atualização"
    echo 4. Disparador: A cada 4 horas
    echo 5. Ação: Iniciar programa
    echo 6. Programa: %~dp0atualizar_dados.py
    echo 7. Argumentos: externo
    echo.
    echo Ou execute manualmente: python atualizar_dados.py externo
) else (
    echo ✅ Tarefa agendada criada com sucesso!
    echo 📅 Atualização automática a cada 4 horas
)

echo.
echo 🚀 Executando primeira atualização...
python atualizar_dados.py externo

echo.
echo ========================================
echo ✅ CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo 📋 O que foi configurado:
echo - ✅ Atualização automática a cada 4 horas
echo - ✅ Primeira atualização executada
echo - ✅ Banco de dados interno criado
echo.
echo 🎯 Para usar o dashboard:
echo 1. Execute: streamlit run dashboard.py
echo 2. Ou use o deploy no Streamlit Cloud
echo.
echo 📊 Para atualizar manualmente:
echo - python atualizar_dados.py externo
echo - python atualizar_dados.py simulado
echo - python atualizar_dados.py verificar
echo.
pause
