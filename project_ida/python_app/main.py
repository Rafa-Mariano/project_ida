from python_app.etl.extractor import Extractor
from python_app.etl.transformer import Transformer
from python_app.config import URL_FONTE, DB_CONFIG
from python_app.etl.loader import Loader
import psycopg2

def main():
    print("Iniciando processo ETL...")
    extractor = Extractor(URL_FONTE)
    transformer = Transformer()
    loader = Loader()

    df_raw = extractor.baixar_dados()
    df_transformed = transformer.transformar(df_raw)
    loader.carregar(df_transformed)
    sql_file = "sql/create_datamart.sql"

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    with open(sql_file, "r", encoding="utf-8") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()

    print("Tabelas criadas com sucesso!")

    print("Processo concluído.")

if __name__ == "__main__":
    main()
