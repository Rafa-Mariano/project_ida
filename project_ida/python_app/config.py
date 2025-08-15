import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

URL_FONTE = os.getenv("URL_FONTE") # Coloquei a url de apenas 1 arquivo para criar o projeto

