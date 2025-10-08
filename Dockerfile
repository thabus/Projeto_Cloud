# 1. Imagem Base: Atualizada para uma versão do Python compatível com o Django 5.x
FROM python:3.12-slim

# 2. Diretório de Trabalho
WORKDIR /app

# Define a variável de ambiente DENTRO do contêiner
ENV AZURE_BLOB_CONNECTION="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://host.docker.internal:10000/devstoreaccount1;"

# 3. Copiar e Instalar Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o Código do Projeto
COPY . .

# 5. Comando de Execução
CMD ["python", "-m", "automacao_b3.extract"]