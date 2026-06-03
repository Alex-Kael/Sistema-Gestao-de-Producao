import streamlit as st
import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            # Evita que o operador fique esperando o app "congelado".
            connect_timeout=5 
        )
        return conexao
    except Error as e:
        # Caso de erro de conexão
        st.divider()
        st.error("⚠️ **Conexão com o Servidor Indisponível**")
        
        st.markdown("""
        Não foi possível estabelecer comunicação com o banco de dados na nuvem. 
        Isso geralmente acontece por dois motivos:
        1. **Instabilidade na sua conexão de internet** local.
        2. **Manutenção temporária** nos servidores da nuvem.
        """)
        
        # Cria um botão de "Tentar Novamente"
        if st.button("🔄 Tentar Conectar Novamente", type="primary", use_container_width=True):
            st.rerun()
            
        st.divider()
        st.stop()