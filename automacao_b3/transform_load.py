# automacao_b3/transform_load.py (VERSÃO FINAL PARA POSTGRESQL)

import io
import logging
import psycopg2
from psycopg2.extras import execute_values
from .azure_storage import get_file_from_blob
from lxml import etree

# --- Configurações ---
FILE_NAME_IN_AZURE = "BVBG.186.01_BV000471202509240001000061923366930.xml" 

# --- CONFIGURAÇÕES DO BANCO DE DADOS POSTGRESQL ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "admin"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

def setup_database():
    """Cria a tabela de negociações se ela não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS negociacoes (
            id SERIAL PRIMARY KEY, ticker TEXT NOT NULL, trade_date DATE,
            open_price NUMERIC, min_price NUMERIC, max_price NUMERIC, close_price NUMERIC
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Banco de dados '{DB_NAME}' e tabela 'negociacoes' prontos.")

def insert_stocks_data(stocks_data):
    """Insere uma lista de dados de ações no banco de dados de forma eficiente."""
    if not stocks_data:
        logging.warning("Nenhum dado para inserir no banco de dados.")
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM negociacoes')
        execute_values(cursor, 
            'INSERT INTO negociacoes (ticker, trade_date, open_price, min_price, max_price, close_price) VALUES %s',
            stocks_data
        )
        conn.commit()
        logging.info(f"{len(stocks_data)} registros inseridos com sucesso no banco de dados.")
    except Exception as e:
        logging.error(f"Erro ao inserir dados no banco: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def transform_and_load():
    setup_database()
    logging.info(f"Baixando o arquivo '{FILE_NAME_IN_AZURE}' do Azurite...")
    xml_content = get_file_from_blob(FILE_NAME_IN_AZURE)
    if not xml_content:
        logging.error("Não foi possível obter o conteúdo do arquivo. Abortando.")
        return
    
    xml_bytes = io.BytesIO(xml_content.encode('utf-8'))
    ns = {'bvmf': 'urn:bvmf.217.01.xsd'}
    context = etree.iterparse(xml_bytes, tag=f"{{{ns['bvmf']}}}PricRpt", huge_tree=True, events=('end',))
    
    logging.info("Iniciando extração e filtragem...")
    filtered_stocks = []

    for _, elem in context:
        scty_id_elem = elem.find('bvmf:SctyId', ns)
        if scty_id_elem is None: continue
        
        tckr_symb_elem = scty_id_elem.find('bvmf:TckrSymb', ns)
        if tckr_symb_elem is None or tckr_symb_elem.text is None: continue
        ticker = tckr_symb_elem.text

        # --- O FILTRO CORRETO E FUNCIONAL ---
        # Filtra pelo tamanho do ticker para pegar apenas o mercado à vista (padrão e fracionário)
        if not (5 <= len(ticker) <= 6):
            elem.clear()
            while elem.getprevious() is not None: del elem.getparent()[0]
            continue
        
        # --- ETAPA DE EXTRAÇÃO (só para os que passaram no filtro) ---
        trade_date_elem = elem.find('bvmf:TradDt/bvmf:Dt', ns)
        trade_date = trade_date_elem.text if trade_date_elem is not None else None

        fin_instrm_attrbts = elem.find('bvmf:FinInstrmAttrbts', ns)
        if fin_instrm_attrbts is None: continue

        opng_pric_elem = fin_instrm_attrbts.find('bvmf:FrstPric', ns)
        open_price = float(opng_pric_elem.text) if opng_pric_elem is not None and opng_pric_elem.text is not None else None

        min_pric_elem = fin_instrm_attrbts.find('bvmf:MinPric', ns)
        min_price = float(min_pric_elem.text) if min_pric_elem is not None and min_pric_elem.text is not None else None

        max_pric_elem = fin_instrm_attrbts.find('bvmf:MaxPric', ns)
        max_price = float(max_pric_elem.text) if max_pric_elem is not None and max_pric_elem.text is not None else None

        clsg_pric_elem = fin_instrm_attrbts.find('bvmf:LastPric', ns)
        close_price = float(clsg_pric_elem.text) if clsg_pric_elem is not None and clsg_pric_elem.text is not None else None
        
        if ticker:
            filtered_stocks.append((ticker, trade_date, open_price, min_price, max_price, close_price))

        elem.clear()
        while elem.getprevious() is not None: del elem.getparent()[0]

    logging.info("Extração e filtragem finalizadas.")
    insert_stocks_data(filtered_stocks)
    logging.info("Processo de transformação e carga concluído.")

if __name__ == "__main__":
    transform_and_load()