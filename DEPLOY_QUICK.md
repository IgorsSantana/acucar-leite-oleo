# 🚀 Deploy Rápido - Streamlit Cloud

## ✅ **Arquivos Necessários (já criados):**
- ✅ `dashboard.py` - App principal
- ✅ `requirements.txt` - Dependências Python
- ✅ `.streamlit/config.toml` - Configurações Streamlit
- ✅ `.streamlit/secrets.toml.example` - Exemplo de secrets

## 🎯 **Passos para Deploy:**

### 1. **Criar Repositório GitHub**
```bash
git init
git add .
git commit -m "Dashboard de análise de vendas"
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

### 2. **Deploy no Streamlit Cloud**
1. Acesse: https://share.streamlit.io/
2. Login com GitHub
3. Clique em "New app"
4. Configure:
   - **Repository**: `SEU-USUARIO/SEU-REPOSITORIO`
   - **Branch**: `main`
   - **Main file path**: `dashboard.py`
   - **App URL**: `dashboard-vendas` (ou nome de sua escolha)

### 3. **Deploy!**
- Clique em "Deploy!"
- Aguarde 2-5 minutos
- URL será: `https://dashboard-vendas.streamlit.app/`

## 🎉 **Pronto!**

O app funcionará em **modo demonstração** com dados simulados.

Para conectar ao banco real, configure os secrets no Streamlit Cloud:
- Settings → Secrets → Cole o conteúdo de `.streamlit/secrets.toml.example`

## 📱 **URL Final:**
`https://dashboard-vendas.streamlit.app/`
