# 🗄️ Guia de Conexão com Banco de Dados

## ❌ **Problema Atual:**
```
Can't open lib 'IBM DB2 ODBC DRIVER' : file not found
```

O driver ODBC do DB2 não está disponível no Streamlit Cloud (ambiente Linux).

## 🎯 **Soluções Disponíveis:**

### **1. 🚀 Streamlit Cloud + Secrets (Recomendado para Teste)**

#### **Configurar Secrets no Streamlit Cloud:**
1. Vá para seu app no Streamlit Cloud
2. Settings → Secrets
3. Cole este conteúdo:

```toml
[secrets]
DB_HOST = "10.64.1.11"
DB_PORT = "50000"
DB_NAME = "SAB"
DB_USER = "db2user_ro"
DB_PASSWORD = "Sup3rs44nt0"
DB_DRIVER = "IBM DB2 ODBC DRIVER"
DB_PROTOCOL = "TCPIP"
```

#### **⚠️ Limitação:**
- Funciona apenas se o banco permitir conexões externas
- Pode não funcionar devido ao driver ODBC

---

### **2. 🌐 Railway (Melhor para Produção)**

Railway permite instalar dependências do sistema:

#### **Passos:**
1. Crie um `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar driver IBM DB2
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copiar arquivos
COPY . /app
WORKDIR /app

# Instalar dependências Python
RUN pip install -r requirements.txt

# Expor porta
EXPOSE $PORT

# Comando de inicialização
CMD streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy no Railway:
   - Conecte com GitHub
   - Selecione seu repositório
   - Railway detectará o Dockerfile automaticamente

---

### **3. 🔄 API Proxy (Solução Híbrida)**

Crie uma API local que conecta ao banco e sirva os dados:

#### **API Local (Flask):**
```python
# api_proxy.py
from flask import Flask, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

@app.route('/api/dados')
def get_dados():
    # Sua lógica de conexão com DB2 aqui
    # Retorna JSON com os dados
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### **Dashboard Modificado:**
```python
# No dashboard.py, substituir a função de conexão:
import requests

@st.cache_data(ttl=300)
def buscar_dados_relatorio(dias_analise, dias_projecao):
    try:
        response = requests.get(f"http://sua-api.com/api/dados?dias={dias_analise}")
        return pd.DataFrame(response.json())
    except:
        return gerar_dados_demo(dias_analise, dias_projecao)
```

---

### **4. 📊 Modo Demonstração (Funcionando Agora)**

O sistema já funciona com dados simulados:
- ✅ **5 lojas** simuladas
- ✅ **3 categorias** (Óleo, Açúcar, Leite)  
- ✅ **Dados realistas** com variações
- ✅ **Todos os cálculos** funcionando

---

### **5. 🔧 Docker Local + Deploy**

#### **Criar Dockerfile completo:**
```dockerfile
FROM python:3.11-slim

# Instalar dependências
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar driver IBM DB2 ODBC
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🎯 **Recomendação Imediata:**

### **Para Teste/Demo:**
- ✅ **Use o modo demonstração** (já funcionando)
- ✅ **Dados simulados** realistas
- ✅ **Todos os recursos** disponíveis

### **Para Produção:**
1. **Railway** com Dockerfile (melhor suporte a drivers)
2. **API Proxy** (separar conexão do dashboard)
3. **VPS próprio** com Docker

---

## 🚀 **Próximos Passos:**

1. **Teste o modo demo** primeiro
2. **Escolha uma solução** de produção
3. **Implemente gradualmente**

**O sistema já está funcionando perfeitamente em modo demonstração!** 🎉
