# 🚀 Guia de Upload para GitHub

## 📋 **Pré-requisitos:**
- ✅ Conta no GitHub
- ✅ Git instalado no seu computador

## 🎯 **Método 1: Script Automático (Windows)**

### **Passos:**
1. **Execute o script:**
   ```bash
   upload_github.bat
   ```

2. **Siga as instruções** na tela

3. **Cole a URL** do seu repositório GitHub quando solicitado

---

## 🎯 **Método 2: Script Automático (Linux/Mac)**

### **Passos:**
1. **Execute o script:**
   ```bash
   ./upload_github.sh
   ```

2. **Siga as instruções** na tela

3. **Cole a URL** do seu repositório GitHub quando solicitado

---

## 🎯 **Método 3: Manual (Passo a Passo)**

### **1. Criar Repositório no GitHub:**
1. Acesse: https://github.com/
2. Clique em **"New"** ou **"+"** → **"New repository"**
3. Configure:
   - **Repository name**: `dashboard-vendas` (ou nome de sua escolha)
   - **Description**: `Dashboard de análise de vendas - Óleo, Açúcar e Leite`
   - **Public** (gratuito)
   - ✅ **Add a README file**
4. Clique em **"Create repository"**

### **2. Copiar URL do Repositório:**
- Copie a URL que aparece (ex: `https://github.com/seu-usuario/dashboard-vendas.git`)

### **3. Configurar Git Localmente:**
```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Dashboard de análise de vendas - Óleo, Açúcar e Leite

- Sistema completo de análise de vendas
- Dados simulados para demonstração  
- Deploy pronto para Streamlit Cloud
- Formatação com ponto como separador
- Unidades em vez de quilogramas
- Cache otimizado para performance
- Interface responsiva e profissional"

# Adicionar remote
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

# Push para GitHub
git push -u origin main
```

---

## 🎯 **Método 4: GitHub Desktop (Interface Gráfica)**

### **Passos:**
1. **Baixe GitHub Desktop**: https://desktop.github.com/
2. **Instale e configure** com sua conta GitHub
3. **Clone** seu repositório criado
4. **Copie os arquivos** para a pasta clonada
5. **Commit e Push** via interface

---

## 📁 **Arquivos que Serão Enviados:**

### ✅ **Arquivos Principais:**
- `dashboard.py` - App principal
- `requirements.txt` - Dependências
- `README.md` - Documentação
- `.streamlit/config.toml` - Configurações Streamlit

### ✅ **Arquivos de Deploy:**
- `Procfile` - Para Railway
- `render.yaml` - Para Render
- `DEPLOY_QUICK.md` - Guia de deploy
- `DATABASE_CONNECTION_GUIDE.md` - Guia de conexão

### ✅ **Scripts:**
- `upload_github.bat` - Script Windows
- `upload_github.sh` - Script Linux/Mac
- `.gitignore` - Arquivos ignorados

### ❌ **Arquivos Ignorados:**
- `.streamlit/secrets.toml` - Configurações sensíveis
- `__pycache__/` - Cache Python
- `.env` - Variáveis de ambiente

---

## 🚀 **Após o Upload:**

### **1. Verificar no GitHub:**
- Acesse seu repositório
- Confirme que todos os arquivos estão lá
- Verifique se o README está aparecendo

### **2. Deploy no Streamlit Cloud:**
1. Acesse: https://share.streamlit.io/
2. **Login** com GitHub
3. **New app**
4. Configure:
   - **Repository**: seu-usuario/dashboard-vendas
   - **Branch**: main
   - **Main file path**: dashboard.py
   - **App URL**: dashboard-vendas (ou nome único)
5. **Deploy!**

### **3. URL Final:**
`https://dashboard-vendas.streamlit.app/`

---

## 🔧 **Troubleshooting:**

### **Erro: "Repository not found"**
- Verifique se o repositório foi criado no GitHub
- Confirme a URL do repositório

### **Erro: "Authentication failed"**
- Configure suas credenciais Git:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### **Erro: "Permission denied"**
- Use token de acesso pessoal do GitHub
- Ou configure SSH keys

---

## 🎉 **Resultado Final:**

Após o upload, você terá:
- ✅ **Repositório no GitHub** com todos os arquivos
- ✅ **Deploy automático** no Streamlit Cloud
- ✅ **URL pública** funcionando
- ✅ **Código versionado** e backup seguro

**Está tudo pronto para o upload!** 🚀
