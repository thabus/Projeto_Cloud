from azure.storage.blob import BlobServiceClient

AZURE_BLOB_CONNECTION = "UseDevelopmentStorage=true"
BLOB_CONTAINER_NAME = "dados_pegrao_b3"

def save_file_to_blob(file_name, local_path_file):
    
    service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION)
    container_client = service.get_container_client(BLOB_CONTAINER_NAME)
    try:
        container_client.create_container()
    except Exception:
        pass  # Container já existe
    
    with open(local_path_file, "rb") as data:
        container_client.upload_blob(name=file_name, data=data, overwrite=True)
    