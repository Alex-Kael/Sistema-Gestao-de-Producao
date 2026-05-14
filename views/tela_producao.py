import streamlit as st
from database.conexao import conectar_banco
from database.consultas import buscar_dados_cadastros
from mysql.connector import Error

def renderizar_producao():
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