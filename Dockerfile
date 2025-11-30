FROM python:3.13-slim

#Define a pasta de trabalho dentro do container
WORKDIR /app

#Como usei a versão slim do python ele não vem com o "curl", logo é instalar ele 
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* 

#Copia os arquivos de requisitos primeiro
COPY requirements.txt .

#Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

#Copia todo o resto do código para dentro do container
COPY . .

#Comando padrão que será sobreescrevido pelo docker compose para usar o uvicorn
CMD ["python", "main.py"]