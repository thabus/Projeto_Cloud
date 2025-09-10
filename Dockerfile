# 1. Imagem Base: Atualizada para uma versão do Python compatível com o Django 5.x
FROM python:3.12-slim

# 2. Diretório de Trabalho
WORKDIR /app

# 3. Copiar e Instalar Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o Código do Projeto
COPY . .

# 5. Comando de Execução
CMD ["python", "automacao_b3/extract.py"]