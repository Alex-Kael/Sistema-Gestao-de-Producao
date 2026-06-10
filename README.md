# 🏭 Sistema Integrado de Controle de Produção

Um sistema web completo, responsivo e seguro desenvolvido em **Python** e **Streamlit** para gerenciar e analisar os lançamentos de produção industrial. O sistema conta com controle de acesso, banco de dados em nuvem e painéis interativos.

## ✨ Funcionalidades Principais

* **🔒 Autenticação e Segurança:** * Sistema de Login blindado.
  * Senhas criptografadas no banco de dados utilizando padrão industrial (**Bcrypt**).
* **👥 Controle de Acesso (RBAC):**
  * **Administrador:** Acesso total a Dashboards, Cadastros e Gestão de Registros.
  * **Operador:** Acesso restrito apenas ao Lançamento de Produção e Histórico.
* **📈 Dashboard Dinâmico:**
  * Métricas de faturamento e passadas totais.
  * Gráficos interativos criados com **Altair**.
  * Filtros de data (Ano e Mês).
  * **Exportação de Dados:** Geração de relatórios com um clique para **Excel (.xlsx)** e **CSV**.
* **📝 Lançamento de Produção:**
  * Formulários dinâmicos que buscam ativamente (em tempo real) as máquinas, operadores, clientes e produtos disponíveis no banco de dados.
  * Cálculo automático de faturamento baseado no produto selecionado.
* **📊 Histórico e Relatórios:**
  * Tabela de dados interativa.
  * **Sistema de Paginação nativo** para lidar de forma leve com grandes volumes de dados.
  * Exclusão de registros incorretos diretamente pela tabela.
* **⚙️ Cadastros Base e Soft Delete:**
  * Gestão em abas para Máquinas, Funcionários, Clientes e Produtos.
  * Utilização de *Soft Delete* (Inativação) para preservar a integridade histórica dos relatórios antigos.
* **🛡️ Resiliência (Tratamento de Quedas):**
  * Tratamento de erros de conexão com a nuvem, prevenindo travamentos e informando o usuário amigavelmente caso a internet ou o banco falhem.

## 🛠️ Tecnologias Utilizadas

* **Front-end / Back-end:** [Python](https://www.python.org/) + [Streamlit](https://streamlit.io/)
* **Banco de Dados:** MySQL (Hospedado na nuvem via [Aiven](https://aiven.io/))
* **Manipulação de Dados:** Pandas
* **Visualização de Dados:** Altair
* **Segurança / Criptografia:** Bcrypt
* **Exportação:** Openpyxl (Excel) e BytesIO

## 📂 Estrutura do Projeto

A arquitetura foi pensada de forma modular, separando as regras de interface, rotas de conexão e autenticação:

```text
📁 projeto_producao/
├── 📄 app.py                  # Arquivo principal (Roteamento e RBAC)
├── 📄 requirements.txt        # Bibliotecas necessárias
├── 📄 README.md               # Documentação do projeto
├── 📁 controllers/
│   └── 📄 auth.py             # Funções de criptografia (bcrypt)
├── 📁 database/
│   ├── 📄 conexao.py          # Conexão com MySQL e tratamento de resiliência
│   └── 📄 consultas.py        # Comandos SQL de leitura e busca (SELECTs)
├── 📁 views/
│   ├── 📄 tela_login.py       # Interface de Autenticação
│   ├── 📄 tela_dashboard.py   # Painel de Gráficos e Exportação
│   ├── 📄 tela_producao.py    # Formulário de Lançamento (INSERT)
│   ├── 📄 tela_relatorio.py   # Tabela paginada e Deleção (DELETE)
│   ├── 📄 tela_cadastros.py   # Adição de cadastros base
│   └── 📄 tela_deletar.py     # Lógica isolada de inativação