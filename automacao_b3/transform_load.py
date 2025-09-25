import io
from azure_storage import get_file_from_blob
from lxml import etree

DATA_FILE = "250923"
FILE_NAME = f"BVBG186_{DATA_FILE}.xml"

def transform_and_load():
    xml_content = get_file_from_blob(FILE_NAME)
    xml_bytes = io.BytesIO(xml_content.encode('utf-8'))

#BUSCAR TckrSymb (nome das Ações)
#BUSCAR TradDtls (Detalhe das Negociações)
#volume financeiro,
#preço maximo,
#preço minimo,
#preço fechamento,
#preço abertura,
#data da negociação

    for _, elemXml in etree.ioterparse(xml_bytes, tag="{urn:bvmf.217.01.xsd}TckrSymb", huge_tree=True ):
        print(f"Ação: {elemXml.text} ")
