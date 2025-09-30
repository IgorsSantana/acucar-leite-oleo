# 🚀 Guia de Deploy Gratuito - Dashboard de Análise

## 📋 Pré-requisitos
- Conta no GitHub
- Conta no Streamlit Cloud (gratuita)

## 🎯 Opção 1: Streamlit Cloud (Recomendado)

### Passo 1: Preparar Repositório
1. Crie um repositório no GitHub
2. Faça upload dos arquivos do projeto:
   - `dashboard.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `packages.txt`
   - `README.md`

### Passo 2: Deploy no Streamlit Cloud
1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Configure:
   - **Repository**: seu-usuario/seu-repositorio
   - **Branch**: main (ou master)
   - **Main file path**: dashboard.py
   - **App URL**: escolha um nome único

### Passo 3: Configurar Secrets (Opcional)
No Streamlit Cloud, vá em "Settings" > "Secrets" e adicione:

```toml
[secrets]
DB_HOST = "10.64.1.11"
DB_PORT = "50000"
DB_NAME = "SAB"
DB_USER = "db2user_ro"
DB_PASSWORD = "Sup3rs44nt0"
```

**⚠️ Nota:** Se não configurar os secrets, o app funcionará em **modo demonstração** com dados simulados.

### Passo 4: Deploy
1. Clique em "Deploy!"
2. Aguarde o build (2-5 minutos)
3. Sua URL estará disponível em: https://seu-app.streamlit.app/

## 🎯 Opção 2: Railway

### Passo 1: Preparar
1. Crie um `Procfile`:
```
web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### Passo 2: Deploy
1. Acesse: https://railway.app/
2. Conecte com GitHub
3. Selecione seu repositório
4. Configure as variáveis de ambiente
5. Deploy automático!

## 🎯 Opção 3: Render

### Passo 1: Preparar
1. Crie um `render.yaml`:
```yaml
services:
  - type: web
    name: dashboard-analise
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### Passo 2: Deploy
1. Acesse: https://render.com/
2. Conecte com GitHub
3. Selecione "New Web Service"
4. Configure e deploy!

## ⚠️ Considerações Importantes

### Banco de Dados
- **Streamlit Cloud** pode ter restrições de conexão externa
- Considere usar um banco na nuvem (PostgreSQL, MySQL)
- Ou use dados mock para demonstração

### Segurança
- **NUNCA** commite senhas no código
- Use variáveis de ambiente sempre
- Considere usar secrets management

### Performance
- Apps gratuitos têm limitações de CPU/memória
- Use cache (`@st.cache_data`) adequadamente
- Otimize queries do banco

## 🔧 Troubleshooting

### Erro de Conexão com Banco
```python
# Adicione no dashboard.py
import os
if 'STREAMLIT_SHARING' in os.environ:
    # Usar dados mock para demo
    st.warning("🚧 Modo demonstração - dados simulados")
else:
    # Usar dados reais
    df = buscar_dados_relatorio()
```

### Erro de Dependências
- Verifique se todas as dependências estão no `requirements.txt`
- Para dependências do sistema, use `packages.txt`

### Timeout
- Reduza o cache TTL
- Otimize as queries
- Use paginação nos dados

## 📱 URLs Finais
Após o deploy, você terá:
- **Streamlit**: https://seu-app.streamlit.app/
- **Railway**: https://seu-app.railway.app/
- **Render**: https://seu-app.onrender.com/

## 🎉 Pronto!
Seu dashboard estará online e acessível de qualquer lugar!
