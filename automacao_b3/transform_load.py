import io
import logging
import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values
from .azure_storage import get_db_connection, get_container_client
from lxml import etree

DB_NAME = "postgres"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_file_for_date(container_client, target_date: datetime):
    """Procura no contêiner do Azurite por um arquivo que contenha a data alvo no nome."""
    date_str_yyyymmdd = target_date.strftime("%Y%m%d")
    logging.info(f"Procurando por arquivo com a data {date_str_yyyymmdd} no Azurite...")

    blob_list = container_client.list_blobs()
    for blob in blob_list:
        if date_str_yyyymmdd in blob.name:
            logging.info(f"Arquivo encontrado: {blob.name}")
            return blob.name
            
    logging.error(f"Nenhum arquivo encontrado para a data {target_date.strftime('%Y-%m-%d')}.")
    return None

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
    logging.info(f"Banco de dados '{DB_NAME}' e tabela 'negociacoes' prontos.")

def insert_stocks_data(stocks_data):
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

def transform_and_load(target_date: datetime):
    setup_database()
    
    container_client = get_container_client()
    file_name_in_azure = find_file_for_date(container_client, target_date)

    if not file_name_in_azure:
        return

    try:
        logging.info(f"Baixando o arquivo '{file_name_in_azure}' do Azurite...")
        blob_client = container_client.get_blob_client(file_name_in_azure)
        xml_content = blob_client.download_blob().readall().decode('utf-8')
    except Exception as e:
        logging.error(f"Não foi possível obter o conteúdo do arquivo '{file_name_in_azure}'. Erro: {e}")
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
            elem.clear()
            while elem.getprevious() is not None: del elem.getparent()[0]
            continue
        
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
    # --- PONTO DE ALTERAÇÃO ---
    # Para testar, vamos usar a data de ontem (07/10)
    data_alvo = datetime(2025, 10, 7)
    transform_and_load(data_alvo)