import streamlit as st
from database.conexao import conectar_banco
from mysql.connector import Error

def renderizar_cadastros():
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
