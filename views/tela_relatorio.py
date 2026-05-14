import streamlit as st
import pandas as pd
import time
from database.conexao import conectar_banco
from database.consultas import buscar_relatorio_producao


def renderizar_relatorio():
    dados_para_tabela = buscar_relatorio_producao() # Função que traz o ID na primeira coluna

    if dados_para_tabela:
        df_delete = pd.DataFrame(
            dados_para_tabela,
            columns=["ID", "Data", "Máquina", "Funcionário", "Cliente", "Produto", "Passadas", "Faturamento"]
        )

        # Exibe a tabela com MODO DE SELEÇÃO ATIVADO
        # hide_index=True esconde o índice do pandas, mas o ID continua no DF
        evento_selecao = st.dataframe(
            df_delete,
            width='stretch',
            hide_index=True,
            on_select="rerun",      # Faz o app atualizar quando clicar na linha
            selection_mode="single-row" # Permite selecionar apenas uma linha por vez
        )

        # 3. Pega a linha selecionada
        linhas_selecionadas = evento_selecao.selection.rows

        if len(linhas_selecionadas) > 0:
            # Recupera o ID do registro a partir da linha clicada
            indice_linha = linhas_selecionadas[0]
            id_para_deletar = df_delete.iloc[indice_linha]["ID"]
            detalhes = df_delete.iloc[indice_linha]

            st.warning(f"⚠️ Você selecionou o registro de: {detalhes['Funcionário']} - {detalhes['Data']}")
            
            if st.button("Confirmar Exclusão Definitiva", type="primary"):
                db = conectar_banco()
                if db:
                    cursor = db.cursor()
                    try:
                        cursor.execute("DELETE FROM registros_producao WHERE id_registros_producao = %s", (int(id_para_deletar),))
                        db.commit()
                        st.success("✅ Registro excluído!")
                        time.sleep(2)
                        st.rerun() # Atualiza para sumir da tabela
                    except Exception as e:
                        st.error(f"Erro: {e}")
                    finally:
                        cursor.close()
                        db.close()
    else:
        st.info("Nenhum registro encontrado.")