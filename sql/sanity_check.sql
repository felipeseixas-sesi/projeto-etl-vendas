-- Sanity checks pré-entrega
-- Objetivo:
-- validar integridade estrutural, KPIs e consistência da Gold

-- TESTE: Totais Silver vs Gold
-- Resultado esperado:
-- volume e receita equivalentes entre Silver e Gold
SELECT 'silver' AS camada, SUM(volume) AS volume, SUM(receita) AS receita
FROM silver_fato_vendas

UNION ALL

SELECT 'gold' AS camada, SUM(volume_total) AS volume, SUM(receita_total) AS receita
FROM vw_market_share;

-- TESTE: Market Share fora da faixa
-- Resultado esperado:
-- 0 linhas retornadas
-- market_share sempre entre 0 e 1
SELECT *
FROM vw_market_share
WHERE market_share < 0
OR market_share > 1;

-- TESTE: Divisões nulas / inconsistências
-- Resultado esperado:
-- 0 linhas retornadas
-- não deve haver volume_total igual a zero
-- não deve haver market_share nulo
SELECT *
FROM vw_market_share
WHERE volume_total = 0
OR market_share IS NULL;

-- TESTE: Amostra rápida dos KPIs
-- Resultado esperado:
-- amostra com KPIs preenchidos e coerentes
-- crescimento_mom pode ser NULL na primeira linha de cada grupo
-- gap_preco e crescimento_mom podem ser positivos ou negativos
SELECT
    ano_mes,
    brick,
    categoria,
    market_share,
    gap_preco,
    crescimento_mom
FROM vw_market_share
LIMIT 15;

--