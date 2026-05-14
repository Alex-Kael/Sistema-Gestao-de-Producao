import streamlit as st
import hashlib

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def gerar_hash(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()