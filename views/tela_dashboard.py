import streamlit as st
import pandas as pd
import altair as alt
from database.consultas import buscar_relatorio_producao

def renderizar_dashboard():
    st.subheader("Indicadores de Produção")

    dados_relatorio = buscar_relatorio_producao()

    if len(dados_relatorio) > 0:
        #Cria o DataFrame do Pandas
        df_dash = pd.DataFrame(
            dados_relatorio, 
            columns=["ID", "Data", "Máquina", "Funcionário", "Cliente", "Produto", "Passadas", "Faturamento"]
        )

        df_dash["Faturamento"] = pd.to_numeric(df_dash["Faturamento"], errors='coerce')
        
        #Converte a coluna Data para o formato oficial de tempo do Pandas
        df_dash["Data"] = pd.to_datetime(df_dash["Data"])
        
        #Extrai o Ano e o Mês para colunas separadas 
        df_dash["Ano"] = df_dash["Data"].dt.year
        df_dash["Mês"] = df_dash["Data"].dt.month
        
        st.markdown("### Filtros")

        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            #Pega todos os anos que existem no banco, remove as duplicatas e ordena do mais novo pro mais velho
            anos_disponiveis = df_dash["Ano"].unique().tolist()
            anos_disponiveis.sort(reverse=True) 
            
            ano_selecionado = st.selectbox("Selecione o Ano:", anos_disponiveis)
            
            #Cria um "sub-dataframe" apenas com os registros do ano selecionado
            df_filtrado = df_dash[df_dash["Ano"] == ano_selecionado]
        
        with col_filtro2:
            # Pega as máquinas únicas DESTE ano, ordena alfabeticamente, e adiciona "Todas" no topo da lista
            lista_maquinas = df_filtrado["Máquina"].unique().tolist()
            lista_maquinas.sort()
            lista_maquinas.insert(0, "Todas") # Coloca "Todas" na posição zero (início)
            
            maquina_selecionada = st.selectbox("Selecione a Máquina:", lista_maquinas)
            
            # Aplica o segundo filtro lógico: Se não for "Todas", corta a tabela só para a máquina escolhida
            if maquina_selecionada != "Todas":
                df_filtrado = df_filtrado[df_filtrado["Máquina"] == maquina_selecionada]

        with col_filtro3:# Mesma lógica da seleção de máquinas
            lista_func = df_filtrado["Funcionário"].unique().tolist()
            lista_func.sort()
            lista_func.insert(0, "Todos")
            
            func_selecionado = st.selectbox("Selecione o Funcionário:", lista_func)
            
            if func_selecionado != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Funcionário"] == func_selecionado]

        st.divider()

        faturamento_total = df_filtrado["Faturamento"].sum()
        passadas_totais = df_filtrado["Passadas"].sum()
        
        # st.columns divide a tela verticalmente
        col1, col2 = st.columns(2)
        col1.metric("Faturamento Total no Ano", f"R$ {faturamento_total:,.2f}")
        col2.metric("Passadas Totais no Ano", f"{passadas_totais}")
        
        # --- ÁREA DO GRÁFICO (Mês a Mês) ---
        st.divider()
        st.markdown(f"### Faturamento Mês a Mês ({ano_selecionado})")
        
        # Agrupa os dados pelo "Mês" e soma a coluna "Faturamento"
        dados_por_mes = df_filtrado.groupby("Mês").agg(
            Faturamento=("Faturamento", "sum"),
            Passadas=("Passadas", "sum")
        ).reset_index()
        
        grafico_barras = alt.Chart(dados_por_mes).mark_bar().encode(
            # Eixo X:coluna "Mês"
            x=alt.X("Mês:N", axis=alt.Axis(labelAngle=0, title="Mês do Ano")),
            
            # Eixo Y:coluna "Faturamento" 
            y=alt.Y("Faturamento:Q", axis=alt.Axis(title="Faturamento (R$)")),
            
            color=alt.value("#1f77b4"),

            tooltip=[
                alt.Tooltip("Mês:N", title="Mês"),
                alt.Tooltip("Faturamento:Q", title="Faturamento (R$)", format=",.2f"),
                alt.Tooltip("Passadas:Q", title="Total de Passadas")
            ] 
        )

        st.altair_chart(grafico_barras, width="stretch")

        st.divider()
        
        # Título ranking1
        if maquina_selecionada == "Todas":
            titulo_ranking = f"### Ranking Máquinas (Faturamento {ano_selecionado})"
        else:
            titulo_ranking = f"### Comparativo da Máquina {maquina_selecionada} no Ano ({ano_selecionado})"
        
        st.markdown(titulo_ranking)
        
        # Agrupa pelo nome da Máquina e soma Faturamento e Passadas
        dados_ranking = df_filtrado.groupby("Máquina").agg(
            Faturamento=("Faturamento", "sum"),
            Passadas=("Passadas", "sum")
        ).reset_index()
        
        # Ordena do maior faturamento para o menor e pega as Top 10
        dados_ranking = dados_ranking.sort_values("Faturamento", ascending=False).head(10)
        
        grafico_ranking = alt.Chart(dados_ranking).mark_bar().encode(
            # Eixo X (Faturamento)
            x=alt.X("Faturamento:Q", title="Faturamento Total (R$)"),
            
            # Eixo Y (Máquina)
            # O parâmetro sort="-x" manda ordenar as máquinas pelo valor do eixo X (Faturamento) de forma decrescente.
            y=alt.Y("Máquina:N", sort="-x", title="Máquina"),
            
            color=alt.value("#ff7f0e"),
            
            # Tooltips para dar detalhes ao passar o mouse
            tooltip=[
                alt.Tooltip("Máquina:N"),
                alt.Tooltip("Faturamento:Q", title="Faturamento (R$)", format=",.2f"),
                alt.Tooltip("Passadas:Q", title="Passadas Totais")
            ]
        ).interactive() # Permite zoom e pan caso o gráfico fique muito grande

        st.altair_chart(grafico_ranking, width="stretch")