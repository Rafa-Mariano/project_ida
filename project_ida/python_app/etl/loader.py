import psycopg2
import pandas as pd
from python_app.config import DB_CONFIG

class Loader:
    """Classe para carregar dados no PostgreSQL"""

    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def carregar(self, df: pd.DataFrame):
        """Insere os dados nas tabelas dimensão e fato"""
        cur = self.conn.cursor()

        for _, row in df.iterrows():
            
            taxa = row['Taxa']
            if taxa == '' or pd.isna(taxa):
                taxa = None  # None vira NULL no banco

            cur.execute("""
                INSERT INTO datamart_ida.dim_tempo (ano, mes, data_ref)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (row['ano'], row['mes'], row['data_ref']))

            cur.execute("""
                INSERT INTO datamart_ida.dim_servico (nome_servico)
                VALUES (%s)
                ON CONFLICT DO NOTHING;
            """, (row['Servico'],))

            cur.execute("""
                INSERT INTO datamart_ida.dim_grupo (nome_grupo)
                VALUES (%s)
                ON CONFLICT DO NOTHING;
            """, (row['Grupo'],))

            cur.execute("""
                INSERT INTO datamart_ida.fact_ida (id_tempo, id_servico, id_grupo, taxa_resolucao_5_dias)
                SELECT t.id_tempo, s.id_servico, g.id_grupo, %s
                FROM datamart_ida.dim_tempo t
                JOIN datamart_ida.dim_servico s ON s.nome_servico = %s
                JOIN datamart_ida.dim_grupo g ON g.nome_grupo = %s
                WHERE t.ano = %s AND t.mes = %s
            """, (
                row['Taxa'],
                row['Servico'],
                row['Grupo'],
                row['ano'],
                row['mes']
            ))

        self.conn.commit()
        cur.close()
        self.conn.close()
