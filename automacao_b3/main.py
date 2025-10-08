import logging
from datetime import datetime
from . import extract
from . import transform_load

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    """
    Orquestra a execução do pipeline de ponta a ponta.
    """
  
    data_alvo = datetime.now()
    #data_alvo = datetime(2025, 9, 25) 
    
    logging.info(f"--- INICIANDO PIPELINE COMPLETO PARA A DATA: {data_alvo.strftime('%Y-%m-%d')} ---")
    
    # 1. Módulo de Extração e Upload para o Blob
    logging.info(">>> FASE 1: Extração <<<")
    xml_filename = extract.run(data_alvo)
    
    # 2. Módulo de Transformação e Carga no Postgres
    if xml_filename:
        logging.info(">>> FASE 2: Transformação e Carga <<<")
        transform_load.transform_and_load(xml_filename)
        logging.info("--- PIPELINE COMPLETO FINALIZADO COM SUCESSO ---")
    else:
        logging.error("--- PIPELINE INTERROMPIDO: A fase de extração falhou. ---")

if __name__ == "__main__":
    run_pipeline()