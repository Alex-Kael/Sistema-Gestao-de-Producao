import streamlit as st
from database.consultas import buscar_dados_cadastros
from controllers.auth import gerar_hash

def renderizar_login():
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
