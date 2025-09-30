# 🗄️ Guia do Banco de Dados Interno

## 🎯 **Visão Geral**

Sistema completo de banco de dados interno SQLite que permite:
- ✅ **Dados reais** do banco externo DB2
- ✅ **Dados simulados** para demonstração
- ✅ **Atualização automática** programada
- ✅ **Qualquer pessoa pode usar** sem configuração

---

## 📁 **Arquivos Criados**

### **🗄️ Gerenciamento de Banco:**
- `database_manager.py` - Classe principal do banco
- `atualizar_dados.py` - Script de atualização
- `dados_vendas.db` - Banco SQLite (criado automaticamente)

### **⏰ Agendamento:**
- `agendar_atualizacao.bat` - Agendador Windows
- `agendar_atualizacao.sh` - Agendador Linux/Mac

### **📊 Dashboard:**
- `dashboard.py` - Modificado para usar banco interno
- `requirements.txt` - Atualizado

---

## 🚀 **Como Usar**

### **1. 📋 Configuração Inicial**

#### **Windows:**
```bash
# Executar o agendador
agendar_atualizacao.bat
```

#### **Linux/Mac:**
```bash
# Dar permissão e executar
chmod +x agendar_atualizacao.sh
./agendar_atualizacao.sh
```

#### **Manual:**
```bash
# Primeira atualização
python atualizar_dados.py externo

# Ou dados simulados
python atualizar_dados.py simulado
```

### **2. 🎯 Usar o Dashboard**

```bash
# Executar dashboard
streamlit run dashboard.py
```

**Funcionalidades no Dashboard:**
- ✅ **Botão de atualização** no sidebar
- ✅ **Dados externos** ou simulados
- ✅ **Última atualização** mostrada
- ✅ **Cache inteligente** (5 minutos)

---

## ⏰ **Atualização Automática**

### **Windows (Task Scheduler):**
- ✅ **A cada 4 horas** automaticamente
- ✅ **Executa em background**
- ✅ **Logs de erro** salvos

### **Linux/Mac (Cron):**
- ✅ **A cada 4 horas** via crontab
- ✅ **Logs automáticos**
- ✅ **Gerenciamento via terminal**

### **Manual:**
```bash
# Dados externos
python atualizar_dados.py externo

# Dados simulados  
python atualizar_dados.py simulado

# Verificar dados
python atualizar_dados.py verificar
```

---

## 🗄️ **Estrutura do Banco**

### **Tabela `vendas`:**
```sql
- id (PRIMARY KEY)
- data_venda (DATE)
- id_loja (INTEGER)
- codigo_subgrupo (INTEGER)
- categoria (TEXT)
- quantidade_vendida (REAL)
- estoque_atual (REAL)
- venda_diaria_media (REAL)
- projecao_venda (REAL)
- compra_recomendada (REAL)
- data_atualizacao (TIMESTAMP)
```

### **Tabela `configuracoes`:**
```sql
- id (PRIMARY KEY)
- chave (TEXT UNIQUE)
- valor (TEXT)
- descricao (TEXT)
- data_atualizacao (TIMESTAMP)
```

---

## 🔄 **Fluxo de Dados**

### **1. Dados Externos (DB2):**
```
DB2 → pyodbc → Processamento → SQLite → Dashboard
```

### **2. Dados Simulados:**
```
Geração → SQLite → Dashboard
```

### **3. Atualização:**
```
Agendador → Script → SQLite → Dashboard (auto-refresh)
```

---

## 📊 **Vantagens do Sistema**

### **✅ Para o Usuário:**
- **Sem configuração** - Funciona imediatamente
- **Dados sempre atualizados** - Atualização automática
- **Fallback inteligente** - Dados simulados se externo falhar
- **Interface amigável** - Botões no dashboard

### **✅ Para o Administrador:**
- **Backup automático** - Banco SQLite local
- **Logs completos** - Acompanhamento de erros
- **Flexibilidade** - Externo ou simulado
- **Performance** - Cache otimizado

### **✅ Para Deploy:**
- **Funciona em qualquer lugar** - SQLite portável
- **Sem dependências externas** - Banco local
- **Deploy simples** - Inclui dados simulados
- **Escalável** - Fácil migração para outros bancos

---

## 🔧 **Comandos Úteis**

### **Verificar Status:**
```bash
python atualizar_dados.py verificar
```

### **Forçar Atualização:**
```bash
python atualizar_dados.py externo
```

### **Dados Demo:**
```bash
python atualizar_dados.py simulado
```

### **Ver Logs:**
```bash
# Windows
type log_atualizacao.txt
type log_erros.txt

# Linux/Mac
cat log_atualizacao.txt
cat log_erros.txt
```

---

## 🚀 **Deploy com Banco Interno**

### **1. Preparar Arquivos:**
```bash
# Incluir no repositório
git add database_manager.py
git add atualizar_dados.py
git add dados_vendas.db
git commit -m "Adicionar banco interno"
git push
```

### **2. Deploy no Streamlit Cloud:**
- ✅ **Funciona automaticamente** com dados simulados
- ✅ **Sem configuração** adicional
- ✅ **Banco incluído** no repositório

### **3. Atualização em Produção:**
```bash
# No servidor, executar:
python atualizar_dados.py externo
```

---

## 🎉 **Resultado Final**

### **✅ Sistema Completo:**
- **Banco interno** funcionando
- **Atualização automática** configurada
- **Dashboard** usando dados locais
- **Deploy** pronto para qualquer lugar

### **✅ Qualquer Pessoa Pode:**
1. **Baixar o projeto**
2. **Executar** `agendar_atualizacao.bat`
3. **Abrir** `streamlit run dashboard.py`
4. **Usar** imediatamente!

### **✅ Dados Sempre Atualizados:**
- **Automático** a cada 4 horas
- **Manual** via botões no dashboard
- **Fallback** para dados simulados

**O sistema está completo e pronto para uso!** 🚀
