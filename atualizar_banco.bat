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
echo 2. Atualizar com dados simulados
echo 3. Verificar status atual
echo 4. Sair
echo.

set /p opcao="Escolha uma opcao (1-4): "

if "%opcao%"=="1" goto externo
if "%opcao%"=="2" goto simulado
if "%opcao%"=="3" goto status
if "%opcao%"=="4" goto sair
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

:simulado
echo.
echo Atualizando com dados simulados...
python atualizar_banco_local.py simulado
echo.
echo Para atualizar o Streamlit Cloud, execute:
echo   git add dados_vendas.db
echo   git commit -m "Atualizar dados simulados"
echo   git push origin main
pause
goto fim

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
