@echo off
echo ============================================================
echo    CONFIGURADOR DE BANCO DE DADOS
echo ============================================================
echo.
echo Este script ira configurar as credenciais do banco DB2.
echo Certifique-se de ter as credenciais corretas antes de continuar.
echo.

set /p continuar="Deseja continuar? (s/n): "

if /i "%continuar%"=="s" goto configurar
if /i "%continuar%"=="sim" goto configurar
if /i "%continuar%"=="y" goto configurar
if /i "%continuar%"=="yes" goto configurar
goto sair

:configurar
echo.
echo Executando configurador...
python configurar_banco.py
echo.
pause
goto fim

:sair
echo.
echo Operacao cancelada.
goto fim

:fim
echo.
echo Processo concluido!
pause
