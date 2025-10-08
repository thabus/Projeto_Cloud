import os
from azure.storage.blob import BlobServiceClient, PublicAccess

# String de conexão PADRÃO para rodar no seu PC (Windows)
LOCAL_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

# O código pega a string da variável de ambiente 'AZURE_BLOB_CONNECTION'.
# Se não encontrar (como ao rodar no Windows), ele usa a string padrão LOCAL_CONNECTION_STRING.
AZURE_BLOB_CONNECTION = os.getenv("AZURE_BLOB_CONNECTION", LOCAL_CONNECTION_STRING)

BLOB_CONTAINER_NAME = "dados-pegrao-b3"

def save_file_to_blob(file_name, local_path_file):
    
    # --- LINHA DE DEBUG ADICIONADA ---
    print(f"--- DEBUG SAVE: Usando Connection String: {AZURE_BLOB_CONNECTION} ---")
    
    service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    container_client = service.get_container_client(BLOB_CONTAINER_NAME)
    try:
        container_client.create_container(public_access=PublicAccess.Container)
    except Exception:
        pass  # Container já existe
    
    with open(local_path_file, "rb") as data:
        container_client.upload_blob(name=file_name, data=data, overwrite=True)
    
    
def get_file_from_blob(file_name):
    
    # --- LINHA DE DEBUG ADICIONADA ---
    print(f"--- DEBUG GET: Usando Connection String: {AZURE_BLOB_CONNECTION} ---")

    service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    container_client = service.get_container_client(BLOB_CONTAINER_NAME)
    try:
        container_client.create_container(public_access=PublicAccess.Container)
    except Exception:
        pass  # Container já existe
    
    # cria a referência ao blob
    blob_client = container_client.get_blob_client(file_name)

    try:
        download_stream = blob_client.download_blob()
        blob_content = download_stream.readall().decode('utf-8')
        return blob_content
    except Exception as e:
        print(f"Erro ao baixar o blob {file_name}: {e}")
        return None