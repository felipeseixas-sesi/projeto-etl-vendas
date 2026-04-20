import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DB_CONFIG, TABLE_NAMES


def get_engine():
    connection_string = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    return create_engine(connection_string)


def test_connection(engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def load_dataframe(df: pd.DataFrame, table_name: str, engine) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )


def load_all(dataframes: dict) -> None:
    engine = get_engine()
    test_connection(engine)

    load_dataframe(dataframes["dim_filial"], TABLE_NAMES["dim_filial"], engine)
    load_dataframe(dataframes["dim_produto"], TABLE_NAMES["dim_produto"], engine)
    load_dataframe(dataframes["fato_vendas"], TABLE_NAMES["fato_vendas"], engine)