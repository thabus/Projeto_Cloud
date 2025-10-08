import os
import requests
import zipfile
import random
import logging
from datetime import datetime
import pandas_market_calendars as mcal
import time

from .azure_storage import save_file_to_blob

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

PATH_TO_SAVE = os.getenv("PATH_TO_SAVE_B3_DATA", "./dados_b3")
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

def is_trading_day(check_date):
    b3_calendar = mcal.get_calendar('B3')
    schedule = b3_calendar.schedule(start_date=check_date, end_date=check_date)
    return not schedule.empty

def build_url_download(date_str_yymmdd):
    return f"https://www.b3.com.br/pesquisapregao/download?filelist=SPRE{date_str_yymmdd}.zip"

def try_http_download(url):
    session = requests.Session()
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        logging.info(f"Tentando baixar de: {url}")
        resp = session.get(url, headers=headers, timeout=60)
        if resp.ok and resp.content and resp.content[:2] == b"PK":
            return resp.content, os.path.basename(url)
        logging.warning(f"Falha no download. Status: {resp.status_code}, Tamanho: {len(resp.content)} bytes.")
    except requests.RequestException as e:
        logging.error(f"Exceção de rede ao acessar a URL {url}: {e}")
    return None, None

def yymmdd(dt: datetime):
    return dt.strftime("%y%m%d")

def run(date_to_process: datetime):
    """
    Executa o processo de extração.
    NOVO: Retorna o nome do principal arquivo XML baixado em caso de sucesso, senão retorna None.
    """
    if not is_trading_day(date_to_process.date()):
        logging.info(f"Data {date_to_process.strftime('%Y-%m-%d')} não é um dia de pregão na B3. Abortando.")
        return None

    dt_str = yymmdd(date_to_process)
    url_to_download = build_url_download(dt_str)
    
    zip_bytes, zip_name = None, None
    for attempt in range(3):
        logging.info(f"Tentativa [{attempt + 1}/3] para baixar o arquivo.")
        zip_bytes, zip_name = try_http_download(url_to_download)
        if zip_bytes:
            logging.info(f"Arquivo de cotações baixado com sucesso: {zip_name}")
            break
        if attempt < 2:
            time.sleep(300) # Espera 5 minutos
    
    if not zip_bytes:
        logging.error("Não foi possível baixar o arquivo de cotações após todas as tentativas.")
        return None

    os.makedirs(PATH_TO_SAVE, exist_ok=True)
    zip_path = os.path.join(PATH_TO_SAVE, f"pregao_{dt_str}.zip")
    with open(zip_path, "wb") as arquivo:
        arquivo.write(zip_bytes)
    
    main_xml_filename = None
    try:
        extract_path = os.path.join(PATH_TO_SAVE, f"SPRE{dt_str}")
        nested_zip_path = os.path.join(PATH_TO_SAVE, f"pregao_{dt_str}")

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(nested_zip_path)
        
        inner_zip_path = os.path.join(nested_zip_path, f"SPRE{dt_str}.zip")
        with zipfile.ZipFile(inner_zip_path, "r") as zf:
            zf.extractall(extract_path)

        logging.info(f"Arquivos extraídos para '{extract_path}'.")

        logging.info("Iniciando upload para o Azure Blob Storage...")
        arquivos = [f for f in os.listdir(extract_path) if f.endswith('.xml')]
        for arquivo in arquivos:
            local_path = os.path.join(extract_path, arquivo)
            # Identifica o arquivo principal (geralmente o maior)
            if "BVBG.186.01" in arquivo:
                 main_xml_filename = arquivo
            logging.info(f"Subindo arquivo para o Azure Blob Storage: {arquivo}")
            save_file_to_blob(arquivo, local_path)
        
        logging.info("Upload para o Azure Blob Storage concluído.")
        return main_xml_filename # RETORNA O NOME DO ARQUIVO PRINCIPAL

    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao extrair ou fazer upload: {e}")
        return None