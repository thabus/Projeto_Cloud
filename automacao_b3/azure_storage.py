import os
import psycopg2
from azure.storage.blob import BlobServiceClient

# --- CONFIGURAÇÕES DO AZURE ---
LOCAL_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
AZURE_BLOB_CONNECTION = os.getenv("AZURE_BLOB_CONNECTION", LOCAL_CONNECTION_STRING)
BLOB_CONTAINER_NAME = "dados-pegrao-b3"

# --- CONFIGURAÇÕES DO POSTGRESQL ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "admin"

def get_container_client():
    """Retorna um cliente para interagir com o contêiner de blob."""
    service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    return service_client.get_container_client(BLOB_CONTAINER_NAME)

def save_file_to_blob(file_name, local_path_file):
    """Salva um arquivo local no blob storage."""
    container_client = get_container_client()
    try:
        if not container_client.exists():
            container_client.create_container(public_access='container')
    except Exception:
        pass
    
    with open(local_path_file, "rb") as data:
        container_client.upload_blob(name=file_name, data=data, overwrite=True)

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )