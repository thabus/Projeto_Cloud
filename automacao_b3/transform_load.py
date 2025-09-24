from azure_storage import get_file_from_blob

DATA_FILE = "20250923"
FILE_NAME = f"BVBG186_{DATA_FILE}.xml"

def transform_and_load():
    xml_content = get_file_from_blob(FILE_NAME)
    print(xml_content)

transform_and_load()