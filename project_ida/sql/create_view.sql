CREATE OR REPLACE VIEW datamart_ida.view_taxa_variacao AS
WITH variacao AS (
    SELECT
        t.ano,
        t.mes,
        g.nome_grupo,
        f.taxa_resolucao_5_dias,
        LAG(f.taxa_resolucao_5_dias) OVER (PARTITION BY g.nome_grupo ORDER BY t.ano, t.mes) AS taxa_anterior,
        ((f.taxa_resolucao_5_dias - LAG(f.taxa_resolucao_5_dias) OVER (PARTITION BY g.nome_grupo ORDER BY t.ano, t.mes)) /
        NULLIF(LAG(f.taxa_resolucao_5_dias) OVER (PARTITION BY g.nome_grupo ORDER BY t.ano, t.mes),0) * 100) AS taxa_variacao
    FROM datamart_ida.fact_ida f
    JOIN datamart_ida.dim_tempo t ON f.id_tempo = t.id_tempo
    JOIN datamart_ida.dim_grupo g ON f.id_grupo = g.id_grupo
)
SELECT
    ano || '-' || LPAD(mes::text, 2, '0') AS mes,
    ROUND(AVG(taxa_variacao), 2) AS taxa_variacao_media,
    JSONB_OBJECT_AGG(nome_grupo, ROUND(taxa_variacao, 2)) AS grupos_variacao
FROM variacao
GROUP BY ano, mes
ORDER BY ano, mes;
