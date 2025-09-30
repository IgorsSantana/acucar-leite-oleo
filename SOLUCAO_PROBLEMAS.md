# 🔧 Solução de Problemas - Sistema de Análise de Vendas

## 🚨 **Problema: Erro de Autenticação no Banco DB2**

### **Erro Típico:**
```
SQL30082N O processamento de segurança falhou com a razão "24" 
("USERNAME AND/OR PASSWORD INVALID"). SQLSTATE=08001
```

### **✅ Solução:**

#### **1. Configurar Credenciais Corretas:**
```bash
# Windows
configurar_banco.bat

# Linux/Mac
python3 configurar_banco.py
```

#### **2. Digite as Credenciais Corretas:**
- **Usuário:** (seu usuário do DB2)
- **Senha:** (sua senha do DB2)

#### **3. Teste a Conexão:**
O script irá testar automaticamente a conexão após salvar as credenciais.

#### **4. Execute a Atualização:**
```bash
python atualizar_banco_local.py externo
```

---

## 🔍 **Outros Problemas Comuns**

### **Problema: Driver ODBC Não Encontrado**
```
Can't open lib 'IBM DB2 ODBC DRIVER' : file not found
```

**✅ Solução:**
1. Instalar IBM DB2 ODBC Driver
2. Verificar se o driver está no PATH
3. Usar driver alternativo se necessário

### **Problema: Timeout de Conexão**
```
Connection timeout
```

**✅ Solução:**
1. Verificar conectividade de rede
2. Verificar se o servidor DB2 está online
3. Verificar firewall/proxy

### **Problema: Banco de Dados Não Encontrado**
```
Database 'SAB' not found
```

**✅ Solução:**
1. Verificar nome do banco
2. Verificar se o banco está acessível
3. Verificar permissões do usuário

---

## 🛠️ **Comandos de Diagnóstico**

### **1. Verificar Status:**
```bash
python atualizar_banco_local.py status
```

### **2. Testar Conexão:**
```bash
python configurar_banco.py
```

### **3. Verificar Logs:**
```bash
# Verificar log de erros
type log_erros.txt

# Verificar log de atualizações
type log_atualizacao.txt
```

---

## 📋 **Checklist de Verificação**

### **Antes de Executar:**
- [ ] IBM DB2 ODBC Driver instalado
- [ ] Conectividade de rede com servidor DB2
- [ ] Credenciais corretas do banco
- [ ] Permissões de acesso ao banco
- [ ] Python e dependências instaladas

### **Durante a Execução:**
- [ ] Conexão estabelecida com sucesso
- [ ] Consulta SQL executada
- [ ] Dados retornados do banco
- [ ] Banco interno atualizado
- [ ] Commit e push realizados

### **Após a Execução:**
- [ ] Dashboard atualizado no Streamlit Cloud
- [ ] Dados visíveis no dashboard
- [ ] Última atualização registrada

---

## 🔐 **Configuração de Credenciais**

### **Arquivo config.py:**
```python
CONFIG_CONEXAO = {
    "DRIVER": "{IBM DB2 ODBC DRIVER}",
    "DATABASE": "SAB",
    "HOSTNAME": "10.64.1.11",
    "PORT": "50000",
    "PROTOCOL": "TCPIP",
    "UID": "seu_usuario",
    "PWD": "sua_senha"
}
```

### **⚠️ Importante:**
- O arquivo `config.py` está no `.gitignore`
- Não compartilhe suas credenciais
- Mantenha o arquivo seguro

---

## 📞 **Suporte**

### **Se o problema persistir:**
1. Verifique os logs de erro
2. Teste a conexão manualmente
3. Verifique com o administrador do banco
4. Confirme as credenciais com a equipe de TI

### **Informações para Suporte:**
- Mensagem de erro completa
- Sistema operacional
- Versão do Python
- Versão do driver ODBC
- Logs de erro (log_erros.txt)
