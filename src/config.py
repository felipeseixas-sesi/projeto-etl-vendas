import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

RAW_DATA_DIR = "data/raw"

TABLE_NAMES = {
    "fato_vendas": "silver_fato_vendas",
    "dim_filial": "silver_dim_filial",
    "dim_produto": "silver_dim_produto",
}