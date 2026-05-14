import streamlit as st
from database.conexao import conectar_banco
from mysql.connector import Error

def buscar_dados_cadastros(tabela, coluna_id, coluna_nome):
    db = conectar_banco()
    if db:
        cursor = db.cursor()
        if tabela == "funcionarios":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "produtos":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "maquinas":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        elif tabela == "clientes":
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela} WHERE ativo = 1;"
        else:
            comando = f"SELECT {coluna_id}, {coluna_nome} FROM {tabela}"

        try:
            cursor.execute(comando)
            lista = cursor.fetchall()
            return lista
        except Error as e:
            st.error(f"Erro ao buscar dados: {e}")
            return []
        finally:
            cursor.close()
            db.close()       

def buscar_relatorio_producao():
    db = conectar_banco()
    if db:
        cursor = db.cursor()
        # Comando SQL completo unindo a tabela de produção com as 4 tabelas de cadastro
        comando_sql = """
            SELECT 
                r.id_registros_producao,
                r.data_producao, 
                m.nome_maquina, 
                f.nome_funcionario, 
                c.nome_clientes, 
                p.nome_produto, 
                r.quantidade_passadas, 
                r.faturamento
            FROM registros_producao r
            INNER JOIN maquinas m ON r.id_maquina = m.id_maquina
            INNER JOIN funcionarios f ON r.id_funcionario = f.id_funcionarios
            INNER JOIN clientes c ON r.id_cliente = c.id_clientes
            INNER JOIN produtos p ON r.id_produto = p.id_produtos
            ORDER BY r.data_producao DESC
        """
        try:
            cursor.execute(comando_sql)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            st.error(f"Erro ao buscar relatório: {e}")
            return []
        finally:
            cursor.close()
            db.close()
    return []
