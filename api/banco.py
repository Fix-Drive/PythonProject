from matplotlib.pyplot import get
from numpy import long
import oracledb
import configurations
import requests


def get_conexao():
    return oracledb.connect(user=configurations.DB_USER, password=configurations.DB_PASSWORD,
                            dsn=configurations.DB_DSN)


def identificar_veiculo_api(placa):
    payload = {
        "placa": placa,
        "login_cpf": configurations.SINESP_LOGIN,
        "login_senha": configurations.SINESP_PASSWORD,
        "token": configurations.SINESP_TOKEN,
        "timeout": 300
    }

    response = requests.post(configurations.SINESP_URL, json=payload)
    response_json = response.json()
    response.close()

    if response_json['code'] == 200:
        # Verifica se 'data' é uma lista e contém pelo menos um elemento
        if isinstance(response_json['data'], list) and len(response_json['data']) > 0:
            dados_veiculo = response_json['data'][0]  # Acessa o primeiro item da lista
            
            return {
                "modelo": dados_veiculo.get("modelo"),  # Acessa o modelo
                "marca": dados_veiculo.get("marca"),    # Acessa a marca
                "ano": dados_veiculo.get("ano"),        # Acessa o ano
                "cor": dados_veiculo.get("cor"),        # Acessa a cor
                "placa": dados_veiculo.get("placa"),    # Acessa a placa
            }
        else:
            raise ValueError("Nenhum dado de veículo encontrado na resposta.")
    elif 600 <= response_json['code'] < 799:
        raise ValueError(f"Erro na consulta: {response_json['code_message']}")
    else:
        raise Exception("Erro inesperado na consulta.")