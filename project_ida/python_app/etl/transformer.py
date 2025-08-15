import pandas as pd

class Transformer:
    """Classe para transformar dados brutos em formato para Data Mart"""

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa e padroniza o DataFrame:
        - converte mês-ano
        - filtra colunas relevantes
        - renomeia para padrão comum
        """
        # Define a linha 9 (índice 8) como cabeçalho
        new_header = df.iloc[7]        # pega a linha 9
        df = df[8:]                   # pega todas as linhas a partir da 10 (índice 9)
        df.columns = new_header       # atribui a linha 9 como novo cabeçalho
        df = df.reset_index(drop=True)  # reseta o índice
        # Faz o melt para despivotar os meses
        df = df.melt(
            id_vars=['GRUPO ECONÔMICO', 'VARIÁVEL'],
            var_name='mes_ano',
            value_name='valor'
        )
        print("Colunas após melt:", df.columns.tolist())
        print(df.head())
        
        # Corrigindo os nomes para minúsculos e sem acento
        df = df.rename(columns={
            'GRUPO ECONÔMICO': 'Grupo',
            'VARIÁVEL': 'Servico',
            'valor': 'Taxa'
        })

        df['data_ref'] = pd.to_datetime(df['mes_ano'], format='%Y-%m')
        df['ano'] = df['data_ref'].dt.year
        df['mes'] = df['data_ref'].dt.month

        # Substituir NaN por string vazia (ou outro valor adequado)
        df['Servico'] = df['Servico'].fillna('')

        # Ou, se for coluna numérica, pode usar 0 ou outro valor padrão
        df['Taxa'] = df['Taxa'].fillna('')
        df['Grupo'] = df['Grupo'].fillna('')
        df['Taxa'] = df['Taxa'].replace('', None)
        df['Taxa'] = df['Taxa'].astype(float)  # se necessário


        # Seleciona colunas úteis
        return df[['ano', 'mes', 'data_ref', 'Servico', 'Grupo', 'Taxa']]
