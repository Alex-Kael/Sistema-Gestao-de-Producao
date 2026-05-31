import streamlit as st
import bcrypt

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def verificar_senha(senha_digitada, hash_do_banco):
    senha_bytes = senha_digitada.encode('utf-8')
    hash_bytes = hash_do_banco.encode('utf-8')
    
    # Retorna True se a senha estiver correta, False se errada
    return bcrypt.checkpw(senha_bytes, hash_bytes)