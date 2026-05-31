import streamlit as st
import pandas as pd
import time
import math
from database.conexao import conectar_banco
from database.consultas import buscar_relatorio_producao

def renderizar_relatorio():
    dados_para_tabela = buscar_relatorio_producao()

    if dados_para_tabela:
        df_delete = pd.DataFrame(
            dados_para_tabela,
            columns=["ID", "Data", "Máquina", "Funcionário", "Cliente", "Produto", "Passadas", "Faturamento"]
        )

        # --- SISTEMA DE PAGINAÇÃO ---
        linhas_por_pagina = 20
        total_linhas = len(df_delete)
        total_paginas = math.ceil(total_linhas / linhas_por_pagina)

        # Inicializa a página atual se ainda não existir
        if 'pagina_atual' not in st.session_state:
            st.session_state['pagina_atual'] = 1

        # Controles visuais da paginação
        st.markdown("### Histórico de Lançamentos")
        col_ant, col_info, col_prox = st.columns([1, 2, 1])
        
        with col_ant:
            if st.button("⬅️ Página Anterior", use_container_width=True):
                if st.session_state['pagina_atual'] > 1:
                    st.session_state['pagina_atual'] -= 1
                    st.rerun()
                    
        with col_info:
            st.markdown(f"<div style='text-align: center; margin-top: 10px;'><b>Página {st.session_state['pagina_atual']} de {total_paginas}</b> (Total: {total_linhas} registros)</div>", unsafe_allow_html=True)
            
        with col_prox:
            if st.button("Próxima Página ➡️", use_container_width=True):
                if st.session_state['pagina_atual'] < total_paginas:
                    st.session_state['pagina_atual'] += 1
                    st.rerun()

        # Fatiar o DataFrame para pegar apenas as 20 linhas da página atual
        inicio = (st.session_state['pagina_atual'] - 1) * linhas_por_pagina
        fim = inicio + linhas_por_pagina
        df_pagina = df_delete.iloc[inicio:fim]

        # Exibe o dataframe fatiado
        evento_selecao = st.dataframe(
            df_pagina,
            width='stretch',
            hide_index=True,
            on_select="rerun",      
            selection_mode="single-row" 
        )

        linhas_selecionadas = evento_selecao.selection.rows

        if len(linhas_selecionadas) > 0:
            indice_linha = linhas_selecionadas[0]
            # Usa o .iloc na df_pagina para deletar o registro correto da tela
            id_para_deletar = df_pagina.iloc[indice_linha]["ID"]
            detalhes = df_pagina.iloc[indice_linha]

            st.warning(f"⚠️ Você selecionou o registro de: **{detalhes['Funcionário']}** - Data: **{detalhes['Data']}**")
            
            if st.button("Confirmar Exclusão Definitiva", type="primary"):
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    try:
                        cursor.execute("DELETE FROM registros_producao WHERE id_registros_producao = %s", (int(id_para_deletar),))
                        db.commit()
                        st.success("✅ Registro excluído!")
                        time.sleep(1)
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Erro: {e}")
                    finally:
                        cursor.close()
                        db.close()
    else:
        st.info("Nenhum lançamento de produção registrado até o momento.")