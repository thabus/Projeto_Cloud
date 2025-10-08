import os
from lxml import etree

# --- CONFIGURAÇÃO ---
NOME_DO_ARQUIVO_XML = "BVBG.186.01_BV000471202509240001000061923366930.xml"
CAMINHO_DO_ARQUIVO = os.path.join('dados_locais', 'SPRE250924', NOME_DO_ARQUIVO_XML)

def investigar_codigos_de_mercado():
    """
    Lê o XML e imprime o Ticker e o Código de Mercado dos primeiros 100 registros.
    """
    print(f"Investigando códigos de mercado em: {CAMINHO_DO_ARQUIVO}\n")

    try:
        ns = {'bvmf': 'urn:bvmf.217.01.xsd'}
        context = etree.iterparse(
            CAMINHO_DO_ARQUIVO, 
            events=('end',),
            tag=f"{{{ns['bvmf']}}}PricRpt"
        )

        print("--- Amostra de Tickers e seus Códigos de Mercado ---")
        
        count = 0
        for event, elem in context:
            # Pega o Ticker
            scty_id_elem = elem.find('bvmf:SctyId', ns)
            ticker = "N/A"
            if scty_id_elem is not None:
                tckr_symb_elem = scty_id_elem.find('bvmf:TckrSymb', ns)
                if tckr_symb_elem is not None:
                    ticker = tckr_symb_elem.text
            
            # Pega o Código de Mercado
            fin_instrm_attrbts = elem.find('bvmf:FinInstrmAttrbts', ns)
            market_code = "NAO_ENCONTRADO"
            if fin_instrm_attrbts is not None:
                mkt_tp_cd_elem = fin_instrm_attrbts.find('bvmf:MktIdrCd', ns)
                if mkt_tp_cd_elem is not None:
                    market_code = mkt_tp_cd_elem.text

            print(f"Ticker: {ticker.ljust(15)} | Código de Mercado: {market_code}")

            # Limpa a memória
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            
            count += 1
            if count >= 100: # Para depois de 100 registros para termos uma boa amostra
                break
        
        print("-------------------------------------------------")

    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em '{CAMINHO_DO_ARQUIVO}'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    investigar_codigos_de_mercado()