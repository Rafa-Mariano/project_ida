import pandas as pd
import requests
from io import StringIO
from io import BytesIO

class Extractor:
    """Classe para extrair dados do portal de dados abertos - Consumidor IDA"""

    def __init__(self, url_csv: str):
        self.url_csv = url_csv

    def baixar_dados(self) -> pd.DataFrame:
        """
        Baixa o CSV da URL fornecida e retorna um DataFrame.
        """
        response = requests.get(self.url_csv)
        response.raise_for_status()

        # Ajustar separador conforme o CSV real: vírgula, ponto-e-vírgula, etc.
        df = pd.read_excel(BytesIO(response.content), engine="odf")
        # Verificar primeiras linhas para validar colunas
        print("Colunas disponíveis:", df.columns.tolist())
        return df
