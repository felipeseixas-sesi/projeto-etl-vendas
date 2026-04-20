import pandas as pd
from src.utils import to_snake_case


EXPECTED_COLUMNS = {
    "fato_vendas": [
        "data", "produto_id", "filial_id", "empresa",
        "volume", "preco_unitario", "receita"
    ],
    "dim_filial": [
        "filial_id", "brick", "regiao", "cluster"
    ],
    "dim_produto": [
        "produto_id", "categoria", "nome_produto"
    ],
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [to_snake_case(col) for col in df.columns]
    return df


def validate_expected_columns(df: pd.DataFrame, dataset_name: str) -> None:
    expected = set(EXPECTED_COLUMNS[dataset_name])
    actual = set(df.columns)

    missing = expected - actual
    extra = actual - expected

    if missing:
        raise ValueError(
            f"{dataset_name}: colunas obrigatórias ausentes: {sorted(missing)}"
        )

    if extra:
        # não quebra por colunas extras nesta fase
        pass


def transform_fato_vendas(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    validate_expected_columns(df, "fato_vendas")

    df = df[EXPECTED_COLUMNS["fato_vendas"]].copy()

    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    df["produto_id"] = df["produto_id"].astype("string").str.strip()
    df["filial_id"] = df["filial_id"].astype("string").str.strip()
    df["empresa"] = df["empresa"].astype("string").str.strip()
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce")
    df["receita"] = pd.to_numeric(df["receita"], errors="coerce")

    df = df.drop_duplicates()

    # nulos críticos
    df = df.dropna(subset=["data", "produto_id", "filial_id"])

    # regra mínima de sanidade
    df = df[
        (df["volume"].fillna(0) >= 0) &
        (df["preco_unitario"].fillna(0) >= 0) &
        (df["receita"].fillna(0) >= 0)
    ]

    # preenchimento simples
    df["empresa"] = df["empresa"].fillna("nao_informado")

    return df

def transform_dim_filial(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    validate_expected_columns(df, "dim_filial")

    df = df[EXPECTED_COLUMNS["dim_filial"]].copy()

    df["filial_id"] = df["filial_id"].astype("string").str.strip()
    df["brick"] = df["brick"].astype("string").str.strip()
    df["regiao"] = df["regiao"].astype("string").str.strip()
    df["cluster"] = df["cluster"].astype("string").str.strip()

    df = df.drop_duplicates()
    df = df.dropna(subset=["filial_id"])

    df["brick"] = df["brick"].fillna("nao_informado")
    df["regiao"] = df["regiao"].fillna("nao_informado")
    df["cluster"] = df["cluster"].fillna("nao_informado")

    return df


def transform_dim_produto(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    validate_expected_columns(df, "dim_produto")

    df = df[EXPECTED_COLUMNS["dim_produto"]].copy()

    df["produto_id"] = df["produto_id"].astype("string").str.strip()
    df["categoria"] = df["categoria"].astype("string").str.strip()
    df["nome_produto"] = df["nome_produto"].astype("string").str.strip()

    df = df.drop_duplicates()
    df = df.dropna(subset=["produto_id"])

    df["categoria"] = df["categoria"].fillna("nao_informado")
    df["nome_produto"] = df["nome_produto"].fillna("nao_informado")

    return df


def validate_referential_integrity(
    fato_vendas: pd.DataFrame,
    dim_filial: pd.DataFrame,
    dim_produto: pd.DataFrame
) -> pd.DataFrame:
    filial_ids_validos = set(dim_filial["filial_id"].dropna().tolist())
    produto_ids_validos = set(dim_produto["produto_id"].dropna().tolist())

    df = fato_vendas.copy()
    df = df[
        df["filial_id"].isin(filial_ids_validos) &
        df["produto_id"].isin(produto_ids_validos)
    ]

    return df


def transform_all(dataframes: dict) -> dict:
    dim_filial = transform_dim_filial(dataframes["dim_filial"])
    dim_produto = transform_dim_produto(dataframes["dim_produto"])
    fato_vendas = transform_fato_vendas(dataframes["fato_vendas"])

    fato_vendas = validate_referential_integrity(
        fato_vendas=fato_vendas,
        dim_filial=dim_filial,
        dim_produto=dim_produto
    )

    return {
        "dim_filial": dim_filial,
        "dim_produto": dim_produto,
        "fato_vendas": fato_vendas,
    }