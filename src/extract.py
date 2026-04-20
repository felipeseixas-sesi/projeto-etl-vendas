import os
import pandas as pd
from src.config import RAW_DATA_DIR


def read_csv_file(filename: str) -> pd.DataFrame:
    filepath = os.path.join(RAW_DATA_DIR, filename)
    return pd.read_csv(filepath)


def extract_all() -> dict:
    return {
        "fato_vendas": read_csv_file("fato_vendas.csv"),
        "dim_filial": read_csv_file("dim_filial.csv"),
        "dim_produto": read_csv_file("dim_produto.csv"),
    }