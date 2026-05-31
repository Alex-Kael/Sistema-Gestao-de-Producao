import streamlit as st
from database.consultas import buscar_dados_cadastros
from controllers.auth import verificar_senha

def renderizar_login():
    with st.container():
        st.title("Acesso ao Sistema")
        usuario_digitado = st.text_input("Usuário")
        senha_digitada = st.text_input("Palavra-passe", type="password")
        
        if st.button("Entrar"):
            # Puxa as informações do banco de dados primeiro
            usuario_DB = buscar_dados_cadastros("usuarios", "id_usuario", "usuario")
            senha_DB = buscar_dados_cadastros("usuarios", "id_usuario", "senha")
            
            if usuario_DB and senha_DB:
                linha_usuario = usuario_DB[0]
                usuario_banco = linha_usuario[1]

                linha_senha = senha_DB[0]
                hash_banco = linha_senha[1]
                
                # Usa a função do bcrypt para verificar a senha
                senha_correta = verificar_senha(senha_digitada, hash_banco)
                
                if usuario_digitado == usuario_banco and senha_correta:
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                st.error("Erro: Nenhum usuário encontrado no banco de dados.")