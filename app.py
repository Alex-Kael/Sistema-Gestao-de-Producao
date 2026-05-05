import streamlit as st
import pandas as pd
import altair as alt
import time
import hashlib
import mysql.connector
from mysql.connector import Error

# Configuração da página para ficar mais larga e com título na aba do navegador
st.set_page_config(page_title="Sistema de Produção", layout="wide")

#Função de Conexão
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        return conexao
    except Error as e:
        st.error(f"Erro de conexão: {e}")
        return None
    
def buscar_dados_cadastros(tabela, coluna_id, coluna_nome):
    db = conectar_banco()
    if db:
        cursor = db.cursor()
        if tabela == "funcionarios":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "produtos":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "maquinas":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "clientes":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        else:
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela}"

        try:
            cursor.execute(comando)
            lista = cursor.fetchall()
            return lista
        except Error as e:
            st.error(f"Erro ao buscar dados: {e}")
            return []
        finally:
            cursor.close()
            db.close()       

def buscar_relatorio_producao():
    db = conectar_banco()
    if db:
        cursor = db.cursor()
        # Comando SQL completo unindo a tabela de produção com as 4 tabelas de cadastro
        comando_sql = """
            SELECT 
                r.id_registros_producao,
                r.data_producao, 
                m.nome_maquina, 
                f.nome_funcionario, 
                c.nome_clientes, 
                p.nome_produto, 
                r.quantidade_passadas, 
                r.faturamento
            FROM registros_producao r
            INNER JOIN maquinas m ON r.id_maquina = m.id_maquina
            INNER JOIN funcionarios f ON r.id_funcionario = f.id_funcionarios
            INNER JOIN clientes c ON r.id_cliente = c.id_clientes
            INNER JOIN produtos p ON r.id_produto = p.id_produtos
            ORDER BY r.data_producao DESC
        """
        try:
            cursor.execute(comando_sql)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            st.error(f"Erro ao buscar relatório: {e}")
            return []
        finally:
            cursor.close()
            db.close()
    return []

# Inicializa a variável de autenticação se ela ainda não existir
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def gerar_hash(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def tela_login():
    with st.container():
        st.title("Acesso ao Sistema")
        usuario_digitado = st.text_input("Usuário")
        senha_digitada = st.text_input("Palavra-passe", type="password")
        
        if st.button("Entrar"):
            # Aplica o hash na senha que o cara acabou de digitar
            hash_digitado = gerar_hash(senha_digitada)
            
            usuario_DB = buscar_dados_cadastros("usuario","id_usuario","usuario")
            linha_usuario = usuario_DB[0]
            usuario_banco = linha_usuario[1]

            senha_DB = buscar_dados_cadastros("usuario","id_usuario","senha")
            linha_senha = senha_DB[0]
            hash_banco = linha_senha[1]
            
            # Compara o hash gerado com o hash que estava guardado
            if usuario_digitado == usuario_banco and hash_digitado == hash_banco:
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

if not st.session_state['autenticado']:
    tela_login()
else:   
    
    #Título Principal
    st.title("Sistema de Gestão de Produção")
    st.divider() # Cria uma linha horizontal para organizar o visual

    #Criando as abas
    aba_cadastros, aba_producao, aba_relatorio, aba_dashboard, aba_delecao = st.tabs([
        "📝 Cadastros Base", 
        "⚙️ Lançar Produção", 
        "📊 Relatório Geral",
        "📈 Dashboard",
        "🗑️ Apagar Dados"
    ])

    with aba_cadastros:
        #Seção de Cadastro de Máquinas
        st.subheader("Cadastro de Nova Maquina")

        with st.form("form_nova_maquina", clear_on_submit=True):
            nome_da_maquina = st.text_input("Nome da Máquina:")
            
            # Botão de envio
            submit_maquina = st.form_submit_button("Salvar Máquina")

            if submit_maquina:
                
                if nome_da_maquina.strip() == "":
                    st.warning("⚠️ O nome da máquina não pode ficar vazio!")
                else:
                    db = conectar_banco()
                    if db:
                        cursor = db.cursor()
                        #%s para evitar erros com aspas e proteger o banco
                        comando_sql = "INSERT INTO maquinas (nome_maquina) VALUES (%s)"
                        valores = (nome_da_maquina,)
                        
                        try:
                            cursor.execute(comando_sql, valores)
                            db.commit() 
                            st.success(f"✅ Máquina '{nome_da_maquina}' cadastrada com sucesso!")
                        except Error as e:
                            st.error(f"Erro ao salvar no banco: {e}")
                        finally:
                            cursor.close()
                            db.close()

        #=====================================================================================================================
        st.subheader("Cadastro de Novo Funcionário")

        with st.form("form_novo_funcionario", clear_on_submit=True):
            nome_do_funcionario = st.text_input("Nome do Funcionário:")
            
            # Botão de envio
            submit_funcionario = st.form_submit_button("Salvar Funcionário")

            if submit_funcionario:
                # Prevenindo campos vazios
                if nome_do_funcionario.strip() == "":
                    st.warning("⚠️ O nome do funcionário não pode ficar vazio!")
                else:
                    db = conectar_banco()
                    if db:
                        cursor = db.cursor()
                        comando_sql = "INSERT INTO funcionarios (nome_funcionario) VALUES (%s)"
                        valores = (nome_do_funcionario,)
                        
                        try:
                            cursor.execute(comando_sql, valores)
                            db.commit() 
                            st.success(f"✅ Funcionário '{nome_do_funcionario}' cadastrado com sucesso!")
                        except Error as e:
                            st.error(f"Erro ao salvar no banco: {e}")
                        finally:
                            cursor.close()
                            db.close()

        #=====================================================================================================================
        st.subheader("Cadastro de Novo Cliente")

        with st.form("form_novo_cliente", clear_on_submit=True):
            nome_do_cliente = st.text_input("Nome do Cliente:")
            
            # Botão de envio
            submit_cliente = st.form_submit_button("Salvar Cliente")

            if submit_cliente:
                # Prevenindo campos vazios
                if nome_do_cliente.strip() == "":
                    st.warning("⚠️ O nome do Cliente não pode ficar vazio!")
                else:
                    db = conectar_banco()
                    if db:
                        cursor = db.cursor()
                        comando_sql = "INSERT INTO clientes (nome_clientes) VALUES (%s)"
                        valores = (nome_do_cliente,)
                        
                        try:
                            cursor.execute(comando_sql, valores)
                            db.commit() 
                            st.success(f"✅ Cliente '{nome_do_cliente}' cadastrado com sucesso!")
                        except Error as e:
                            st.error(f"Erro ao salvar no banco: {e}")
                        finally:
                            cursor.close()
                            db.close()

        #=====================================================================================================================
        st.subheader("Cadastro de Novo Produto")

        with st.form("form_novo_Produto", clear_on_submit=True):
            nome_do_produto = st.text_input("Nome do Produto:")
            
            # Botão de envio
            submit_produto = st.form_submit_button("Salvar Produto")

            if submit_produto:
                # Prevenindo campos vazios
                if nome_do_produto.strip() == "":
                    st.warning("⚠️ O nome do Produto não pode ficar vazio!")
                else:
                    db = conectar_banco()
                    if db:
                        cursor = db.cursor()
                        comando_sql = "INSERT INTO produtos (nome_produto) VALUES (%s)"
                        valores = (nome_do_produto,)
                        
                        try:
                            cursor.execute(comando_sql, valores)
                            db.commit() 
                            st.success(f"✅ Produto '{nome_do_produto}' cadastrado com sucesso!")
                        except Error as e:
                            st.error(f"Erro ao salvar no banco: {e}")
                        finally:
                            cursor.close()
                            db.close()

    #=====================================================================================================================

    with aba_producao:
        st.subheader("Cadastro de Producao")

        
        data_producao = st.date_input("Data da producao:")

        #busca as listas do DB
        maquina_producao = buscar_dados_cadastros("maquinas", "id_maquina", "nome_maquina")
        if not maquina_producao:
            st.warning("⚠️ Você precisa cadastrar ao menos uma Máquina antes de lançar a produção.")
        else:
            maquina_selecionada = st.selectbox("Maquina", maquina_producao, index=None, format_func=lambda x: x[1])

        funcionario_producao = buscar_dados_cadastros("funcionarios", "id_funcionarios", "nome_funcionario")
        if not funcionario_producao:
            st.warning("⚠️ Você precisa cadastrar ao menos um Funcionário antes de lançar a produção.")
        else:
            funcionario_seleciondado = st.selectbox("Funcionario", funcionario_producao, index=None, format_func=lambda x: x[1])

        clientes_producao = buscar_dados_cadastros("clientes", "id_clientes", "nome_clientes")
        if not clientes_producao:
            st.warning("⚠️ Você precisa cadastrar ao menos um Cliente antes de lançar a produção.")
        else:
            clientes_selecionado = st.selectbox("Cliente", clientes_producao, index=None, format_func=lambda x: x[1])

        produtos_producao = buscar_dados_cadastros("produtos", "id_produtos", "nome_produto")
        if not produtos_producao:
            st.warning("⚠️ Você precisa cadastrar ao menos um Produto antes de lançar a produção.")
        else:
            produtos_selecionado = st.selectbox("Produto", produtos_producao, index=None, format_func=lambda x: x[1])

        passadas_producao = st.number_input("Quantidade de Passadas", min_value=1, step=1)
        preco_producao = st.number_input("Preço (R$)", min_value=0.0, format="%.3f")
        faturamento_producao = passadas_producao * preco_producao
        st.info(f"Faturamento: **R$ {faturamento_producao:,.2f}**")

        data_formatada_producao = data_producao.strftime("%Y-%m-%d")#formatar data para o insert no DB
        

        if st.button("Salvar Produção", type="primary"):
            # Prevenindo campos vazios
            if len(maquina_producao) <= 0 or len(funcionario_producao) <= 0 or len(clientes_producao) <= 0 or len(produtos_producao) <= 0 or passadas_producao == 0 or preco_producao == 0.0:
                st.warning("⚠️ Não pode haver campos vazios!")
            else:
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    comando_sql = "INSERT INTO registros_producao (data_producao, id_maquina, id_funcionario, id_cliente, id_produto, quantidade_passadas, faturamento, preco) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    valores = (data_formatada_producao, maquina_selecionada[0], funcionario_seleciondado[0], clientes_selecionado[0], produtos_selecionado[0], passadas_producao, faturamento_producao, preco_producao,)
                    
                    try:
                        cursor.execute(comando_sql, valores)
                        db.commit() 
                        st.success(f"✅ Producao cadastrada com sucesso!")
                    except Error as e:
                        st.error(f"Erro ao salvar no banco: {e}")
                    finally:
                        cursor.close()
                        db.close()

    #=====================================================================================================================

    with aba_relatorio:
        # --- SEÇÃO DE RELATÓRIO GERAL ---
        st.divider()
        st.subheader("📊 Relatório Geral de Produção")

        # 1. Buscamos os dados (certifique-se que a função retorna o ID)
        dados_para_tabela = buscar_relatorio_producao() # Função que traz o ID na primeira coluna

        if dados_para_tabela:
            df_delete = pd.DataFrame(
                dados_para_tabela,
                columns=["ID", "Data", "Máquina", "Funcionário", "Cliente", "Produto", "Passadas", "Faturamento"]
            )

            # Exibe a tabela com MODO DE SELEÇÃO ATIVADO
            # hide_index=True esconde o índice do pandas, mas o ID continua no DF
            evento_selecao = st.dataframe(
                df_delete,
                width='stretch',
                hide_index=True,
                on_select="rerun",      # Faz o app atualizar quando clicar na linha
                selection_mode="single-row" # Permite selecionar apenas uma linha por vez
            )

            # 3. Pega a linha selecionada
            linhas_selecionadas = evento_selecao.selection.rows

            if len(linhas_selecionadas) > 0:
                # Recupera o ID do registro a partir da linha clicada
                indice_linha = linhas_selecionadas[0]
                id_para_deletar = df_delete.iloc[indice_linha]["ID"]
                detalhes = df_delete.iloc[indice_linha]

                st.warning(f"⚠️ Você selecionou o registro de: {detalhes['Funcionário']} - {detalhes['Data']}")
                
                if st.button("Confirmar Exclusão Definitiva", type="primary"):
                    db = conectar_banco()
                    if db:
                        cursor = db.cursor()
                        try:
                            cursor.execute("DELETE FROM registros_producao WHERE id_registros_producao = %s", (int(id_para_deletar),))
                            db.commit()
                            st.success("✅ Registro excluído!")
                            time.sleep(2)
                            st.rerun() # Atualiza para sumir da tabela
                        except Exception as e:
                            st.error(f"Erro: {e}")
                        finally:
                            cursor.close()
                            db.close()
        else:
            st.info("Nenhum registro encontrado.")

    #=====================================================================================================================

    with aba_dashboard:
        st.subheader("Indicadores de Produção")
        
        dados_relatorio = buscar_relatorio_producao()
        
        if len(dados_relatorio) > 0:
            #Cria o DataFrame do Pandas
            df_dash = pd.DataFrame(
                dados_relatorio, 
                columns=["ID", "Data", "Máquina", "Funcionário", "Cliente", "Produto", "Passadas", "Faturamento"]
            )

            df_dash["Faturamento"] = pd.to_numeric(df_dash["Faturamento"], errors='coerce')
            
            #Converte a coluna Data para o formato oficial de tempo do Pandas
            df_dash["Data"] = pd.to_datetime(df_dash["Data"])
            
            #Extrai o Ano e o Mês para colunas separadas 
            df_dash["Ano"] = df_dash["Data"].dt.year
            df_dash["Mês"] = df_dash["Data"].dt.month
            
            st.markdown("### Filtros")

            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                #Pega todos os anos que existem no banco, remove as duplicatas e ordena do mais novo pro mais velho
                anos_disponiveis = df_dash["Ano"].unique().tolist()
                anos_disponiveis.sort(reverse=True) 
                
                ano_selecionado = st.selectbox("Selecione o Ano:", anos_disponiveis)
                
                #Cria um "sub-dataframe" apenas com os registros do ano selecionado
                df_filtrado = df_dash[df_dash["Ano"] == ano_selecionado]
            
            with col_filtro2:
                # Pega as máquinas únicas DESTE ano, ordena alfabeticamente, e adiciona "Todas" no topo da lista
                lista_maquinas = df_filtrado["Máquina"].unique().tolist()
                lista_maquinas.sort()
                lista_maquinas.insert(0, "Todas") # Coloca "Todas" na posição zero (início)
                
                maquina_selecionada = st.selectbox("Selecione a Máquina:", lista_maquinas)
                
                # Aplica o segundo filtro lógico: Se não for "Todas", corta a tabela só para a máquina escolhida
                if maquina_selecionada != "Todas":
                    df_filtrado = df_filtrado[df_filtrado["Máquina"] == maquina_selecionada]

            with col_filtro3:# Mesma lógica da seleção de máquinas
                lista_func = df_filtrado["Funcionário"].unique().tolist()
                lista_func.sort()
                lista_func.insert(0, "Todos")
                
                func_selecionado = st.selectbox("Selecione o Funcionário:", lista_func)
                
                if func_selecionado != "Todos":
                    df_filtrado = df_filtrado[df_filtrado["Funcionário"] == func_selecionado]

            st.divider()

            faturamento_total = df_filtrado["Faturamento"].sum()
            passadas_totais = df_filtrado["Passadas"].sum()
            
            # st.columns divide a tela verticalmente
            col1, col2 = st.columns(2)
            col1.metric("Faturamento Total no Ano", f"R$ {faturamento_total:,.2f}")
            col2.metric("Passadas Totais no Ano", f"{passadas_totais}")
            
            # --- ÁREA DO GRÁFICO (Mês a Mês) ---
            st.divider()
            st.markdown(f"### Faturamento Mês a Mês ({ano_selecionado})")
            
            # Agrupa os dados pelo "Mês" e soma a coluna "Faturamento"
            dados_por_mes = df_filtrado.groupby("Mês").agg(
                Faturamento=("Faturamento", "sum"),
                Passadas=("Passadas", "sum")
            ).reset_index()
            
            grafico_barras = alt.Chart(dados_por_mes).mark_bar().encode(
                # Eixo X:coluna "Mês"
                x=alt.X("Mês:N", axis=alt.Axis(labelAngle=0, title="Mês do Ano")),
                
                # Eixo Y:coluna "Faturamento" 
                y=alt.Y("Faturamento:Q", axis=alt.Axis(title="Faturamento (R$)")),
                
                color=alt.value("#1f77b4"),

                tooltip=[
                    alt.Tooltip("Mês:N", title="Mês"),
                    alt.Tooltip("Faturamento:Q", title="Faturamento (R$)", format=",.2f"),
                    alt.Tooltip("Passadas:Q", title="Total de Passadas")
                ] 
            )

            st.altair_chart(grafico_barras, width="stretch")

            st.divider()
            
            # Título ranking1
            if maquina_selecionada == "Todas":
                titulo_ranking = f"### Ranking Máquinas (Faturamento {ano_selecionado})"
            else:
                titulo_ranking = f"### Comparativo da Máquina {maquina_selecionada} no Ano ({ano_selecionado})"
            
            st.markdown(titulo_ranking)
            
            # Agrupa pelo nome da Máquina e soma Faturamento e Passadas
            dados_ranking = df_filtrado.groupby("Máquina").agg(
                Faturamento=("Faturamento", "sum"),
                Passadas=("Passadas", "sum")
            ).reset_index()
            
            # Ordena do maior faturamento para o menor e pega as Top 10
            dados_ranking = dados_ranking.sort_values("Faturamento", ascending=False).head(10)
            
            grafico_ranking = alt.Chart(dados_ranking).mark_bar().encode(
                # Eixo X (Faturamento)
                x=alt.X("Faturamento:Q", title="Faturamento Total (R$)"),
                
                # Eixo Y (Máquina)
                # O parâmetro sort="-x" manda ordenar as máquinas pelo valor do eixo X (Faturamento) de forma decrescente.
                y=alt.Y("Máquina:N", sort="-x", title="Máquina"),
                
                color=alt.value("#ff7f0e"),
                
                # Tooltips para dar detalhes ao passar o mouse
                tooltip=[
                    alt.Tooltip("Máquina:N"),
                    alt.Tooltip("Faturamento:Q", title="Faturamento (R$)", format=",.2f"),
                    alt.Tooltip("Passadas:Q", title="Passadas Totais")
                ]
            ).interactive() # Permite zoom e pan caso o gráfico fique muito grande

            st.altair_chart(grafico_ranking, width="stretch")

            #======================================================================================================

            st.divider()
            
            # Título ranking2
            if func_selecionado == "Todos":
                titulo_ranking2 = f"### Ranking Funcionários (Faturamento {ano_selecionado})"
            else:
                titulo_ranking2 = f"### Comparativo do Funcionário {func_selecionado} no Ano ({ano_selecionado})"
            
            st.markdown(titulo_ranking2)
            
            # Agrupa pelo nome do Funcionário e soma Faturamento e Passadas
            dados_ranking2 = df_filtrado.groupby("Funcionário").agg(
                Faturamento=("Faturamento", "sum"),
                Passadas=("Passadas", "sum")
            ).reset_index()
            
            # Ordena do maior faturamento para o menor e pega os Top 10
            dados_ranking2 = dados_ranking2.sort_values("Faturamento", ascending=False).head(10)
            
            grafico_ranking2 = alt.Chart(dados_ranking2).mark_bar().encode(
                # Eixo X (Faturamento)
                x=alt.X("Faturamento:Q", title="Faturamento Total (R$)"),
                
                # Eixo Y (Funcionário)
                # O parâmetro sort="-x" manda ordenar os funcionários pelo valor do eixo X (Faturamento) de forma decrescente.
                y=alt.Y("Funcionário:N", sort="-x", title="Funcionário"),
                
                color=alt.value("#ff160e"),
                
                # Tooltips para dar detalhes ao passar o mouse
                tooltip=[
                    alt.Tooltip("Funcionário:N"),
                    alt.Tooltip("Faturamento:Q", title="Faturamento (R$)", format=",.2f"),
                    alt.Tooltip("Passadas:Q", title="Passadas Totais")
                ]
            ).interactive() # Permite zoom e pan caso o gráfico fique muito grande

            st.altair_chart(grafico_ranking2, width="stretch")
            
        else:
            st.warning("Não há dados de produção cadastrados para gerar o dashboard.")

    #=====================================================================================================================

    with aba_delecao:
        st.subheader("Deleção de Funcionário")

        with st.form("form_deletar_funcionario", clear_on_submit=True):
            funcionario_producao = buscar_dados_cadastros("funcionarios", "id_Funcionarios", "nome_Funcionario")
            nome_do_funcionario = st.selectbox("Funcionário", funcionario_producao, index=None, format_func=lambda x: x[1])
            
            # Botão de envio
            submit_funcionario = st.form_submit_button("Deletar Funcionário")

            if submit_funcionario: 
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    # Usando %s para evitar erros com aspas e proteger o banco
                    comando_sql = "UPDATE funcionarios SET ativo = 0 WHERE id_funcionarios = %s"
                    valores = (nome_do_funcionario[0],) 
                    
                    try:
                        cursor.execute(comando_sql, valores)
                        db.commit() # O commit é o que efetivamente SALVA no banco
                        st.success(f"✅ Funcionário '{nome_do_funcionario}' deletado com sucesso!")
                    except Error as e:
                        st.error(f"Erro ao deletar no banco: {e}")
                    finally:
                        cursor.close()
                        db.close()

        st.subheader("Deleção de Produto")

        with st.form("form_deletar_produto", clear_on_submit=True):
            produtos_producao = buscar_dados_cadastros("produtos", "id_produtos", "nome_produto")
            nome_do_produto = st.selectbox("Produto", produtos_producao, index=None, format_func=lambda x: x[1])
            
            submit_produto = st.form_submit_button("Deletar Produto")

            if submit_produto: 
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    
                    comando_sql = "UPDATE produtos SET ativo = 0 WHERE id_produtos = %s"
                    valores = (nome_do_produto[0],) 
                    
                    try:
                        cursor.execute(comando_sql, valores)
                        db.commit() 
                        st.success(f"✅ Produto '{nome_do_produto}' deletado com sucesso!")
                    except Error as e:
                        st.error(f"Erro ao deletar no banco: {e}")
                    finally:
                        cursor.close()
                        db.close()

        st.subheader("Deleção de Máquina")

        with st.form("form_deletar_maquina", clear_on_submit=True):
            maquina_producao = buscar_dados_cadastros("maquinas", "id_maquina", "nome_maquina")
            nome_da_maquina = st.selectbox("Máquina", maquina_producao, index=None, format_func=lambda x: x[1])
            
            submit_produto = st.form_submit_button("Deletar Máquina")

            if submit_produto: 
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    
                    comando_sql = "UPDATE maquinas SET ativo = 0 WHERE id_maquina = %s"
                    valores = (nome_da_maquina[0],) 
                    
                    try:
                        cursor.execute(comando_sql, valores)
                        db.commit() 
                        st.success(f"✅ Máquina '{nome_da_maquina}' deletada com sucesso!")
                    except Error as e:
                        st.error(f"Erro ao deletar no banco: {e}")
                    finally:
                        cursor.close()
                        db.close()

        st.subheader("Deleção de Clientes")

        with st.form("form_deletar_cliente", clear_on_submit=True):
            clientes_producao = buscar_dados_cadastros("clientes", "id_clientes", "nome_clientes")
            nome_do_cliente = st.selectbox("Clientes", clientes_producao, index=None, format_func=lambda x: x[1])
            
            submit_produto = st.form_submit_button("Deletar Cliente")

            if submit_produto: 
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    
                    comando_sql = "UPDATE clientes SET ativo = 0 WHERE id_clientes = %s"
                    valores = (nome_do_cliente[0],) 
                    
                    try:
                        cursor.execute(comando_sql, valores)
                        db.commit() 
                        st.success(f"✅ Cliente '{nome_do_cliente}' deletado com sucesso!")
                    except Error as e:
                        st.error(f"Erro ao deletar no banco: {e}")
                    finally:
                        cursor.close()
                        db.close()
