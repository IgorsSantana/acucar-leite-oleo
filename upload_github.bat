@echo off
echo ========================================
echo    UPLOAD PARA GITHUB - DASHBOARD
echo ========================================
echo.

REM Verificar se git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git não está instalado ou não está no PATH
    echo Baixe em: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git encontrado!

REM Inicializar repositório se não existir
if not exist ".git" (
    echo.
    echo 🔧 Inicializando repositório Git...
    git init
    echo ✅ Repositório inicializado!
)

REM Adicionar todos os arquivos
echo.
echo 📁 Adicionando arquivos...
git add .
echo ✅ Arquivos adicionados!

REM Fazer commit
echo.
echo 💾 Fazendo commit...
git commit -m "Dashboard de análise de vendas - Óleo, Açúcar e Leite

- Sistema completo de análise de vendas
- Dados simulados para demonstração
- Deploy pronto para Streamlit Cloud
- Formatação com ponto como separador
- Unidades em vez de quilogramas
- Cache otimizado para performance
- Interface responsiva e profissional"

echo ✅ Commit realizado!

REM Configurar remote se não existir
echo.
echo 🌐 Configurando repositório remoto...
echo.
echo Por favor, cole a URL do seu repositório GitHub:
echo Exemplo: https://github.com/seu-usuario/dashboard-vendas.git
echo.
set /p REPO_URL="URL do repositório: "

if "%REPO_URL%"=="" (
    echo ❌ URL não fornecida. Execute novamente e forneça a URL.
    pause
    exit /b 1
)

REM Verificar se remote já existe
git remote -v | findstr "origin" >nul 2>&1
if errorlevel 1 (
    echo 🔗 Adicionando remote origin...
    git remote add origin %REPO_URL%
) else (
    echo 🔄 Atualizando remote origin...
    git remote set-url origin %REPO_URL%
)

echo ✅ Remote configurado!

REM Push para GitHub
echo.
echo 🚀 Enviando para GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  Tentando com branch 'master'...
    git push -u origin master
)

echo.
echo ========================================
echo ✅ UPLOAD CONCLUÍDO COM SUCESSO!
echo ========================================
echo.
echo 🌐 Seu repositório está disponível em:
echo %REPO_URL%
echo.
echo 🚀 Para fazer deploy no Streamlit Cloud:
echo 1. Acesse: https://share.streamlit.io/
echo 2. Login com GitHub
echo 3. New app → Selecione seu repositório
echo 4. Main file: dashboard.py
echo 5. Deploy!
echo.
pause
