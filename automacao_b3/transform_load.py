import io
import logging
import psycopg2
import os # NOVO: importado para ler variáveis de ambiente
from psycopg2.extras import execute_values
from .azure_storage import get_file_from_blob
from lxml import etree

# --- CONFIGURAÇÕES DO BANCO DE DADOS POSTGRESQL ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD") # A senha virá do ambiente

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    if not DB_PASSWORD:
        raise ValueError("A variável de ambiente DB_PASSWORD não foi definida.")
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

def setup_database():
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

def insert_stocks_data(stocks_data):
    if not stocks_data: return
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM negociacoes') # ATENÇÃO: Limpa a tabela antes de inserir.
        execute_values(cursor, 
            'INSERT INTO negociacoes (ticker, trade_date, open_price, min_price, max_price, close_price) VALUES %s',
            stocks_data
        )
        conn.commit()
        logging.info(f"{len(stocks_data)} registros inseridos com sucesso.")
    finally:
        cursor.close()
        conn.close()

# MODIFICAÇÃO: A função agora recebe o nome do arquivo como parâmetro
def transform_and_load(xml_filename: str):
    setup_database()
    logging.info(f"Baixando o arquivo '{xml_filename}' do Azurite...")
    xml_content = get_file_from_blob(xml_filename)
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

        if not (5 <= len(ticker) <= 6):
            elem.clear(); continue
        
        trade_date_elem = elem.find('bvmf:TradDt/bvmf:Dt', ns)
        trade_date = trade_date_elem.text if trade_date_elem is not None else None

        fin_instrm_attrbts = elem.find('bvmf:FinInstrmAttrbts', ns)
        if fin_instrm_attrbts is None: continue

        opng_pric_elem = fin_instrm_attrbts.find('bvmf:FrstPric', ns)
        open_price = opng_pric_elem.text if opng_pric_elem is not None else None

        min_pric_elem = fin_instrm_attrbts.find('bvmf:MinPric', ns)
        min_price = min_pric_elem.text if min_pric_elem is not None else None

        max_pric_elem = fin_instrm_attrbts.find('bvmf:MaxPric', ns)
        max_price = max_pric_elem.text if max_pric_elem is not None else None

        clsg_pric_elem = fin_instrm_attrbts.find('bvmf:LastPric', ns)
        close_price = clsg_pric_elem.text if clsg_pric_elem is not None else None
        
        if ticker:
            filtered_stocks.append((ticker, trade_date, open_price, min_price, max_price, close_price))

        elem.clear()

    logging.info("Extração e filtragem finalizadas.")
    insert_stocks_data(filtered_stocks)
    logging.info("Processo de transformação e carga concluído.")