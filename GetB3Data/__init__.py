# GetB3Data/__init__.py

import logging
import azure.functions as func
import os
import psycopg2
import json

# --- CONFIGURAÇÕES DO BANCO DE DADOS POSTGRESQL ---
# LÊ AS MESMAS VARIÁVEIS DE AMBIENTE QUE O SEU PIPELINE JÁ USA
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    if not DB_PASSWORD:
        raise ValueError("Variáveis de ambiente do banco de dados não configuradas.")
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requisição HTTP para GetB3Data recebida.')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Executa a consulta no banco de dados
        cursor.execute("SELECT ticker, trade_date, open_price, min_price, max_price, close_price FROM negociacoes ORDER BY ticker")
        
        # Pega os nomes das colunas
        column_names = [desc[0] for desc in cursor.description]
        
        # Formata os resultados como uma lista de dicionários (perfeito para JSON)
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
            
        cursor.close()
        conn.close()

        # Converte os dados para JSON. 
        # 'default=str' ajuda a converter datas/números (tipo 'Decimal') para string.
        json_data = json.dumps(data, default=str)

        # Retorna a resposta HTTP com o JSON
        return func.HttpResponse(
            body=json_data,
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Erro ao buscar dados da API: {e}")
        return func.HttpResponse(
             f"Erro interno do servidor: {e}",
             status_code=500
        )