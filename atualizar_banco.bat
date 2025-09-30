@echo off
echo ============================================================
echo    ATUALIZADOR LOCAL - BANCO DE DADOS
echo ============================================================
echo.
echo Este script atualiza o banco interno que sera usado
echo pelo dashboard publico no Streamlit Cloud.
echo.

:menu
echo.
echo Opcoes:
echo 1. Atualizar com dados externos (DB2)
echo 2. Verificar status atual
echo 3. Sair
echo.

set /p opcao="Escolha uma opcao (1-3): "

if "%opcao%"=="1" goto externo
if "%opcao%"=="2" goto status
if "%opcao%"=="3" goto sair
echo Opcao invalida! Tente novamente.
goto menu

:externo
echo.
echo Atualizando com dados externos...
python atualizar_banco_local.py externo
echo.
echo Para atualizar o Streamlit Cloud, execute:
echo   git add dados_vendas.db
echo   git commit -m "Atualizar dados do banco externo"
echo   git push origin main
pause
goto fim

REM Função de dados simulados removida - apenas dados reais

:status
echo.
echo Verificando status...
python atualizar_banco_local.py status
pause
goto fim

:sair
echo.
echo Ate logo!
goto fim

:fim
echo.
echo Processo concluido!
pause
