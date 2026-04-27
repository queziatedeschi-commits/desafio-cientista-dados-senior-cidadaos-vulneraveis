SELECT
    CAST(ch.data_particao AS DATE) AS data_particao,
    ch.tipo,
    ch.id_bairro,
    dim.id_regiao_administrativa,
    COUNT(ch.id_chamado) AS volume_chamados
FROM {{ ref('stg_chamado_1746') }} ch
INNER JOIN {{ ref('stg_dim_territorio') }} dim
    ON ch.id_bairro = dim.id_bairro
GROUP BY
    CAST(ch.data_particao AS DATE),
    ch.tipo,
    ch.id_bairro,
    dim.id_regiao_administrativa