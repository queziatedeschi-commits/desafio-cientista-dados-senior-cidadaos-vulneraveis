import requests
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

def buscar_clima_historico(latitude: float, longitude: float, data_inicio: str, data_fim: str):
    """
    Objetivo:
        Consultar a API Open-Meteo para obter dados históricos diários de clima
        (temperatura média e precipitação) para uma localização específica.
    Parâmetros:
        latitude (float): Latitude do ponto de interesse.
        longitude (float): Longitude do ponto de interesse.
        data_inicio (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.
    Retorno:
        pd.DataFrame: DataFrame contendo as colunas:
            - data_particao (datetime): Data da observação
            - temperatura (float): Temperatura média diária (°C)
            - precipitacao (float): Precipitação diária acumulada (mm)
            - latitude (float): Latitude utilizada na consulta
            - longitude (float): Longitude utilizada na consulta
    Erros:
        TypeError:
            - Se latitude/longitude não forem numéricos
            - Se data_inicio/data_fim não forem strings
        ValueError:
            - Se latitude/longitude forem nulos
            - Se o intervalo de datas for inválido
        requests.exceptions.RequestException:
            - Falha na conexão com a API
        Exception:
            - Resposta inesperada da API (ex: ausência da chave 'daily')
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        raise TypeError("Latitude e longitude devem ser numéricos (int ou float).")

    if latitude is None or longitude is None:
        raise ValueError("Latitude e longitude não podem ser nulos.")

    if not isinstance(data_inicio, str) or not isinstance(data_fim, str):
        raise TypeError("Datas devem ser informadas como string no formato 'YYYY-MM-DD'.")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={data_inicio}"
        f"&end_date={data_fim}"
        "&daily=temperature_2m_mean,precipitation_sum"
        "&timezone=America%2FSao_Paulo")

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Erro ao conectar na API Open-Meteo: {e}")

    dados = response.json()

    if "daily" not in dados:
        raise Exception("Resposta inválida da API: chave 'daily' não encontrada.")
    if not dados["daily"]:
        raise ValueError("Resposta da API vazia para o período informado.")


    df_clima = pd.DataFrame(dados["daily"])
    # Conversão de data
    df_clima["time"] = pd.to_datetime(df_clima["time"])
    # Padronização de nomes de colunas
    df_clima = df_clima.rename(columns={
        "time": "data_particao",
        "temperature_2m_mean": "temperatura",
        "precipitation_sum": "precipitacao"})
    # Adicionando contexto geográfico
    df_clima["latitude"] = latitude
    df_clima["longitude"] = longitude

    return df_clima   



def buscar_feriados(ano: int, pais: str = "BR") -> pd.DataFrame:
    """
    Objetivo:
        Buscar feriados nacionais via API pública.
    Parâmetros:
        ano (int): Ano de consulta.
        pais (str): Código do país (ex: 'BR').
    Retorno:
        pd.DataFrame: DataFrame com datas e nomes dos feriados.
    """

    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/{pais}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao buscar feriados: {e}")

    df = pd.DataFrame(response.json())

    df["data_particao"] = pd.to_datetime(df["date"])

    df = df.rename(columns={
        "localName": "nome_feriado_local",
        "name": "nome_feriado"
    })

    return df[["data_particao", "nome_feriado", "nome_feriado_local"]]

def classificar_dia(row: pd.Series):
    """
    Objetivo:
        Classificar o tipo de dia com base na presença de feriado e eventos extremos.
    Parâmetros:
        row (pd.Series): Linha do DataFrame contendo as colunas 'eh_feriado' e 'evento_extremo'.
    Retorno:
        str: Classificação do dia, podendo ser 'Feriado', 'Evento extremo' ou 'Dia normal'.
    """
    if row["eh_feriado"]:
        return "Feriado"
    elif row["evento_extremo"]:
        return "Evento extremo"
    else:
        return "Dia normal"

def classificar_dimensao(feature: str):
    """
    Objetivo:
        Classificar a variável (feature) de acordo com a dimensão analítica a que pertence,
        como território, clima ou tempo.
    Parâmetros:
        feature (str): Nome da variável a ser classificada.
    Retorno:
        str: Dimensão da variável, podendo ser 'Território', 'Clima', 'Tempo' ou 'Outros'.
    """
    if feature.startswith("nome_bairro") or feature.startswith("nome_regiao_administrativa"):
        return "Território"
    elif feature in ["temperatura", "precipitacao"]:
        return "Clima"
    elif feature in ["mes", "dia_semana", "fim_de_semana", "eh_feriado"]:
        return "Tempo"
    else:
        return "Outros"


def avaliar(modelo, X_test, y_test, nome: str):
    """
    Objetivo:
        Avaliar o desempenho de um modelo de classificação utilizando métricas
        de precisão, recall, F1-score e AUC.
    Parâmetros:
        modelo: Modelo treinado com métodos 'predict' e 'predict_proba'.
        X_test (array-like): Conjunto de dados de teste (features).
        y_test (array-like): Valores reais do conjunto de teste (target).
        nome (str): Nome do modelo avaliado.
    Retorno:
        dict: Dicionário contendo o nome do modelo e as métricas de desempenho:
              'precision', 'recall', 'f1' e 'auc'.
    """
    y_pred = modelo.predict(X_test)
    y_proba = modelo.predict_proba(X_test)[:,1]

    return {
        "modelo": nome,
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "auc": roc_auc_score(y_test, y_proba)
    }