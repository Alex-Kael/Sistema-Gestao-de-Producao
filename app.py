import streamlit as st

# Importando as telas da pasta views
from views.tela_login import renderizar_login
from views.tela_cadastros import renderizar_cadastros
from views.tela_producao import renderizar_producao
from views.tela_relatorio import renderizar_relatorio
from views.tela_dashboard import renderizar_dashboard
from views.tela_deletar import renderizar_delecao

st.set_page_config(page_title="Sistema de Produção", layout="wide")

# Controle de sessão para Login
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    renderizar_login() # Mostra só o login se não estiver autenticado
else:

    #Título Principal
    st.title("Sistema de Gestão de Produção")
    st.divider() # Cria uma linha horizontal para organizar o visual
    
    # Criando as Abas do Sistema
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        "📝 Cadastros Base", 
        "⚙️ Lançar Produção", 
        "📊 Relatório Geral",
        "📈 Dashboard",
        "🗑️ Apagar Dados"
    ])
    
    # Distribuindo as telas dentro de cada aba correspondente
    with aba1:
        renderizar_cadastros()
        
    with aba2:
        renderizar_producao()
        
    with aba3:
        renderizar_relatorio()
        
    with aba4:
        renderizar_dashboard()

    with aba5:
        renderizar_delecao()
        