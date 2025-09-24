from azure.storage.blob import BlobServiceClient

AZURE_BLOB_CONNECTION = "UseDevelopmentStorage=true"
BLOB_CONTAINER_NAME = "dados-pegrao-b3"

def save_file_to_blob(file_name, local_path_file):
    
    service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    container_client = service.get_container_client(BLOB_CONTAINER_NAME)
    try:
        container_client.create_container(BLOB_CONTAINER_NAME, public_access=PublicAccess.Container)
    except Exception:
        pass  # Container já existe
    
    with open(local_path_file, "rb") as data:
        container_client.upload_blob(name=file_name, data=data, overwrite=True)
    
def get_file_from_blob(file_name):
    
    service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    container_client = service.get_container_client(BLOB_CONTAINER_NAME)
    try:
        container_client.create_container(BLOB_CONTAINER_NAME, public_access=PublicAccess.Container)
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