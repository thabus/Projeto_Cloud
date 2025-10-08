import os
import requests
import zipfile
import random
import logging
from datetime import datetime
import pandas_market_calendars as mcal
import time

from .azure_storage import save_file_to_blob
from .helpers import yymmdd
import shutil

# 1. Configuração de Logging para melhor diagnóstico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 2. Caminho para salvar os dados, usando variável de ambiente para flexibilidade
PATH_TO_SAVE = os.getenv("PATH_TO_SAVE_B3_DATA", "./dados_b3")

# 3. Lista de User-Agents para simular um navegador real e evitar bloqueios simples
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

def is_trading_day(check_date):
    
    # Verifica se a data fornecida é um dia de pregão na B3.
    b3_calendar = mcal.get_calendar('B3')
    try:
        schedule = b3_calendar.schedule(start_date=check_date, end_date=check_date)
        return not schedule.empty
    except Exception:
        return False

def build_url_download(date_str_yymmdd):
  
    # Constrói a URL de download para a data especificada.
    return f"https://www.b3.com.br/pesquisapregao/download?filelist=SPRE{date_str_yymmdd}.zip"

def try_http_download(url):
    """
    Tenta baixar o conteúdo da URL com User-Agent rotativo.
    Retorna (content, filename) em caso de sucesso, ou (None, None) em caso de falha.
    """
    session = requests.Session()
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        logging.info(f"Tentando baixar de: {url}")
        resp = session.get(url, headers=headers, timeout=60) 
        
        if resp.ok and resp.content and len(resp.content) > 200:
            if resp.content[:2] == b"PK":
                return resp.content, os.path.basename(url)
            else:
                logging.warning("Conteúdo recebido não parece ser um arquivo ZIP.")
        else:
            logging.warning(f"Falha no download. Status: {resp.status_code}, Tamanho: {len(resp.content)} bytes.")

    except requests.RequestException as e:
        logging.error(f"Exceção de rede ao acessar a URL {url}: {e}")

    return None, None

def run(date_to_process: datetime):
    """
    Executa o processo de extração para uma data específica, com lógica de retentativa.
    """
    if not is_trading_day(date_to_process.date()):
        logging.info(f"Data {date_to_process.strftime('%Y-%m-%d')} não é um dia de pregão na B3. Abortando.")
        return

    dt_str = yymmdd(date_to_process)
    url_to_download = build_url_download(dt_str)
        
    zip_bytes, zip_name = None, None
    max_retries = 3
    retry_delay_seconds = 300  # 5 minutos

    for attempt in range(max_retries):
        logging.info(f"Tentativa [{attempt + 1}/{max_retries}] para baixar o arquivo.")
        
        # 1) Tenta o Download
        zip_bytes, zip_name = try_http_download(url_to_download)

        if zip_bytes:
            logging.info(f"Arquivo de cotações baixado com sucesso: {zip_name}")
            break
        
        if attempt < max_retries - 1:
            logging.warning(f"Falha ao baixar. Próxima tentativa em {retry_delay_seconds / 60} minutos.")
            time.sleep(retry_delay_seconds)
        else:
            logging.error("Não foi possível baixar o arquivo de cotações após todas as tentativas. A execução será interrompida.")
            return

    # 2) Salvar o Zip
    os.makedirs(PATH_TO_SAVE, exist_ok=True)
    zip_path = os.path.join(PATH_TO_SAVE, f"pregao_{dt_str}.zip")
    with open(zip_path, "wb") as arquivo:
        arquivo.write(zip_bytes)
    logging.info(f"Arquivo ZIP salvo em {zip_path}")

    # 3) Extrair os arquivos do zip
    try:
        extract_path_1 = os.path.join(PATH_TO_SAVE, f"pregao_{dt_str}")
        extract_path_2 = os.path.join(PATH_TO_SAVE, f"SPRE{dt_str}")
        
        # Extrai o primeiro ZIP
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_path_1)

        # O arquivo da B3 é um ZIP dentro de outro ZIP
        nested_zip_path = os.path.join(extract_path_1, f"SPRE{dt_str}.zip")
        with zipfile.ZipFile(nested_zip_path, "r") as zf:
            zf.extractall(extract_path_2)

        logging.info(f"Arquivos extraídos do ZIP com sucesso para os diretórios '{extract_path_1}' e '{extract_path_2}'.")
    except zipfile.BadZipFile:
        logging.error(f"O arquivo {zip_path} não é um ZIP válido ou está corrompido.")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao extrair os arquivos: {e}")

    # 4) Fazer upload e Limpar
    try:
        logging.info("Iniciando upload para o Azure Blob Storage...")
        arquivos = [f for f in os.listdir(extract_path_2) if os.path.isfile(os.path.join(extract_path_2, f))]

        if not arquivos:
            logging.warning(f"Nenhum arquivo encontrado em {extract_path_2} para fazer upload.")
            return

        for arquivo in arquivos:
            local_path = os.path.join(extract_path_2, arquivo)
            logging.info(f"Subindo arquivo para o Azure Blob Storage: {arquivo}")
            save_file_to_blob(arquivo, local_path)
        
        logging.info("Upload para o Azure Blob Storage concluído com sucesso.")

    except FileNotFoundError:
        logging.error(f"Diretório de extração não encontrado: {extract_path_2}. Upload cancelado.")
    except Exception as e:
        logging.error(f"Ocorreu um erro durante o upload para o Azure: {e}")

def yymmdd(dt: datetime):
    """Retorna a data no formato YYMMDD."""
    return dt.strftime("%y%m%d")

if __name__ == "__main__":
    # 7. O script pode ser facilmente executado para qualquer data
    #data_alvo = datetime.now()
    data_alvo = datetime(2025, 9, 24)

    logging.info(f"--- Iniciando pipeline de extração para a data: {data_alvo.strftime('%Y-%m-%d')} ---")
    run(data_alvo)
    logging.info("--- Pipeline de extração finalizado. ---")