import logging
import azure.functions as func
# MUDANÇA: Renomeamos a importação de 'main' para 'pipeline_main'
from automacao_b3 import main as pipeline_main

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Gatilho de tempo do Azure Function executado.')
    
    try:
        # MUDANÇA: Chamamos a função a partir do novo nome 'pipeline_main'
        pipeline_main.run_pipeline()
        logging.info('Pipeline da B3 executado com sucesso.')
    except Exception as e:
        logging.error(f"Ocorreu um erro ao executar o pipeline: {e}")