import streamlit as st
from database.consultas import buscar_dados_cadastros
from controllers.auth import verificar_senha

def renderizar_login():
    with st.container():
        st.title("Acesso ao Sistema")
        usuario_digitado = st.text_input("Usuário").strip() # .strip() evita espaços acidentais no input
        senha_digitada = st.text_input("Palavra-passe", type="password")
        
        if st.button("Entrar"):
            usuario_DB = buscar_dados_cadastros("usuarios", "id_usuario", "usuario")
            senha_DB = buscar_dados_cadastros("usuarios", "id_usuario", "senha")
            
            if usuario_DB and senha_DB:
                usuario_banco = None
                hash_banco = None
                
                # Transforma a lista de senhas num dicionário {id: hash} para facilitar a busca             
                dicionario_senhas = {linha[0]: linha[1] for linha in senha_DB}
                
                # Percorre a lista de usuários para achar a linha do usuário digitado
                for linha in usuario_DB:
                    id_user = linha[0]
                    nome_user = linha[1]
                    
                    if nome_user == usuario_digitado:
                        usuario_banco = nome_user
                        # Usa o ID para pegar o hash correspondente desse mesmo usuário
                        hash_banco = dicionario_senhas.get(id_user)
                        break 
                              
                if usuario_banco and hash_banco:
                    senha_correta = verificar_senha(senha_digitada, hash_banco)
                    
                    if senha_correta:
                        st.session_state['autenticado'] = True
                        st.session_state['perfil'] = usuario_banco 
                        st.success("Logado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                st.error("Erro: Nenhum usuário encontrado no banco de dados.")