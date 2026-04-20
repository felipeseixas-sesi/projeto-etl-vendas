CREATE OR REPLACE VIEW vw_market_share AS
WITH base AS (
    SELECT
        TO_CHAR(date_trunc('month', fv.data::timestamp), 'YYYY-MM') AS ano_mes,
        df.brick,
        dp.categoria,
        fv.empresa,
        fv.volume,
        fv.receita
    FROM silver_fato_vendas fv
    INNER JOIN silver_dim_filial df
        ON fv.filial_id = df.filial_id
    INNER JOIN silver_dim_produto dp
        ON fv.produto_id = dp.produto_id
),
agregada AS (
    SELECT
        ano_mes,
        brick,
        categoria,

        SUM(volume) AS volume_total,
        SUM(receita) AS receita_total,

        SUM(CASE WHEN LOWER(empresa) = 'clamed' THEN volume ELSE 0 END) AS volume_clamed,
        SUM(CASE WHEN LOWER(empresa) = 'concorrente' THEN volume ELSE 0 END) AS volume_concorrente,

        SUM(CASE WHEN LOWER(empresa) = 'clamed' THEN receita ELSE 0 END) AS receita_clamed,
        SUM(CASE WHEN LOWER(empresa) = 'concorrente' THEN receita ELSE 0 END) AS receita_concorrente

    FROM base
    GROUP BY
        ano_mes,
        brick,
        categoria
),
kpis AS (
    SELECT
        ano_mes,
        brick,
        categoria,
        volume_total,
        receita_total,
        volume_clamed,
        volume_concorrente,
        receita_clamed,
        receita_concorrente,

        CASE
            WHEN volume_total = 0 THEN 0
            ELSE volume_clamed / NULLIF(volume_total, 0)
        END AS market_share,

        CASE
            WHEN volume_clamed = 0 THEN 0
            ELSE receita_clamed / NULLIF(volume_clamed, 0)
        END AS preco_medio_clamed,

        CASE
            WHEN volume_concorrente = 0 THEN 0
            ELSE receita_concorrente / NULLIF(volume_concorrente, 0)
        END AS preco_medio_concorrente

    FROM agregada
)
SELECT
    ano_mes,
    brick,
    categoria,
    volume_total,
    receita_total,
    volume_clamed,
    volume_concorrente,
    receita_clamed,
    receita_concorrente,
    market_share,
    preco_medio_clamed,
    preco_medio_concorrente,
    (preco_medio_clamed - preco_medio_concorrente) AS gap_preco,
    CASE
        WHEN LAG(volume_total) OVER (
            PARTITION BY brick, categoria
            ORDER BY ano_mes
        ) IS NULL THEN NULL
        WHEN LAG(volume_total) OVER (
            PARTITION BY brick, categoria
            ORDER BY ano_mes
        ) = 0 THEN NULL
        ELSE (
            (volume_total - LAG(volume_total) OVER (
                PARTITION BY brick, categoria
                ORDER BY ano_mes
            )) / NULLIF(LAG(volume_total) OVER (
                PARTITION BY brick, categoria
                ORDER BY ano_mes
            ), 0)
        )
    END AS crescimento_mom
FROM kpis;