# 🔄 Fluxo de Trabalho - Sistema de Análise de Vendas

## 🎯 **Visão Geral do Sistema**

O sistema funciona com **dois ambientes**:

1. **🌐 Streamlit Cloud** - Dashboard público (sempre online)
2. **💻 Seu Computador** - Atualização de dados (quando necessário)

## 📊 **Fluxo de Funcionamento**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Seu PC        │    │   GitHub        │    │ Streamlit Cloud │
│                 │    │                 │    │                 │
│ 1. Executa      │───▶│ 2. Commit +     │───▶│ 3. Atualiza     │
│    atualizacao  │    │    Push         │    │    automatico   │
│                 │    │                 │    │                 │
│ dados_vendas.db │    │ dados_vendas.db │    │ dados_vendas.db │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Como Usar o Sistema**

### **Passo 1: Atualizar Dados no Seu Computador**

#### **Windows:**
```bash
# Execute o script batch
atualizar_banco.bat

# Ou execute diretamente
python atualizar_banco_local.py externo
```

#### **Linux/Mac:**
```bash
# Execute o script shell
./atualizar_banco.sh

# Ou execute diretamente
python3 atualizar_banco_local.py externo
```

### **Passo 2: Enviar para o Streamlit Cloud**

```bash
# Adicionar o banco atualizado
git add dados_vendas.db

# Fazer commit
git commit -m "Atualizar dados do banco externo"

# Enviar para o GitHub
git push origin main
```

### **Passo 3: Streamlit Cloud Atualiza Automaticamente**

- O Streamlit Cloud detecta o push
- Baixa o novo `dados_vendas.db`
- O dashboard mostra os dados atualizados

## ⚙️ **Comandos Disponíveis**

### **Atualização de Dados:**

```bash
# Dados do banco externo (DB2)
python atualizar_banco_local.py externo

# Dados simulados
python atualizar_banco_local.py simulado

# Verificar status atual
python atualizar_banco_local.py status
```

### **Envio para o Cloud:**

```bash
# Atualização completa
git add dados_vendas.db
git commit -m "Atualizar dados - $(date)"
git push origin main
```

## 📋 **Opções de Atualização**

### **1. Dados Externos (Recomendado)**
- ✅ Conecta ao banco DB2
- ✅ Dados reais de vendas
- ✅ Atualização completa
- ⚠️ Requer conexão com o banco

### **2. Dados Simulados**
- ✅ Funciona offline
- ✅ Dados de demonstração
- ✅ Teste rápido
- ⚠️ Não são dados reais

## 🔍 **Verificação de Status**

```bash
# Verificar dados atuais
python atualizar_banco_local.py status
```

**Exemplo de saída:**
```
📊 Verificando status do banco...
✅ 15 registros encontrados

📋 Resumo por categoria:
         QUANTIDADE_VENDIDA  COMPRA_RECOMENDADA
CATEGORIA                                      
AÇÚCAR                    3200               680
LEITE                     1800               450
ÓLEO                      1500               320

📅 Última atualização: 2024-01-15T10:30:00
🔗 Fonte dos dados: externos
```

## 🎯 **Cenários de Uso**

### **Cenário 1: Atualização Diária**
```bash
# Todo dia pela manhã
atualizar_banco.bat
# Escolher opção 1 (dados externos)
# Fazer commit e push
```

### **Cenário 2: Teste Rápido**
```bash
# Para testar o sistema
python atualizar_banco_local.py simulado
git add dados_vendas.db
git commit -m "Teste com dados simulados"
git push origin main
```

### **Cenário 3: Verificação**
```bash
# Verificar se está tudo OK
python atualizar_banco_local.py status
```

## 📱 **Acesso ao Dashboard**

- **URL:** https://acucar-leite-oleo-8xkxt4rahmvpgppqrvumsu.streamlit.app/
- **Acesso:** Público (qualquer pessoa pode ver)
- **Atualização:** Automática após push no GitHub

## 🔧 **Solução de Problemas**

### **Problema: Banco não atualiza no Streamlit**
```bash
# Verificar se o commit foi feito
git status

# Verificar se o push foi feito
git log --oneline -5

# Forçar atualização
git push origin main --force
```

### **Problema: Erro de conexão com DB2**
```bash
# Usar dados simulados como fallback
python atualizar_banco_local.py simulado
```

### **Problema: Script não executa**
```bash
# Windows
python atualizar_banco_local.py externo

# Linux/Mac
python3 atualizar_banco_local.py externo
```

## 📊 **Resumo do Fluxo**

1. **💻 Seu PC:** Executa `atualizar_banco_local.py externo`
2. **📤 GitHub:** Faz commit e push do `dados_vendas.db`
3. **🌐 Streamlit:** Detecta mudanças e atualiza automaticamente
4. **👥 Usuários:** Veem dados atualizados no dashboard público

**Resultado:** Sistema sempre atualizado e acessível publicamente! 🎉
