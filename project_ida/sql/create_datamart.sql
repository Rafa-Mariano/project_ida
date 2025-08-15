-- Criando schema
CREATE SCHEMA IF NOT EXISTS datamart_ida;

-- Dimensão Tempo
CREATE TABLE datamart_ida.dim_tempo (
    id_tempo SERIAL PRIMARY KEY,
    ano INT NOT NULL,
    mes INT NOT NULL,
    data_ref DATE NOT NULL
);
COMMENT ON TABLE datamart_ida.dim_tempo IS 'Dimensão de tempo para análises IDA';

-- Dimensão Serviço
CREATE TABLE datamart_ida.dim_servico (
    id_servico SERIAL PRIMARY KEY,
    nome_servico VARCHAR(100) NOT NULL
);
COMMENT ON TABLE datamart_ida.dim_servico IS 'Serviços como Telefonia Celular, Banda Larga, etc.';

-- Dimensão Grupo Econômico
CREATE TABLE datamart_ida.dim_grupo (
    id_grupo SERIAL PRIMARY KEY,
    nome_grupo VARCHAR(100) NOT NULL
);
COMMENT ON TABLE datamart_ida.dim_grupo IS 'Grupos econômicos (CLARO, ALGAR, etc.)';

-- Fato IDA
CREATE TABLE datamart_ida.fact_ida (
    id_fato SERIAL PRIMARY KEY,
    id_tempo INT REFERENCES datamart_ida.dim_tempo(id_tempo),
    id_servico INT REFERENCES datamart_ida.dim_servico(id_servico),
    id_grupo INT REFERENCES datamart_ida.dim_grupo(id_grupo),
    taxa_resolucao_5_dias NUMERIC(5,2) NOT NULL
);
COMMENT ON TABLE datamart_ida.fact_ida IS 'Valores do IDA por mês, serviço e grupo econômico';
