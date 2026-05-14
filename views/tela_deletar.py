import streamlit as st
from mysql.connector import Error
from database.conexao import conectar_banco
from database.consultas import buscar_dados_cadastros

def renderizar_delecao():
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