from matplotlib.pyplot import get
import oracledb
import requests
DB_USER = "rm558830"
DB_PASSWORD = "070306"
DB_DSN = "oracle.fiap.com.br/orcl"

SINESP_URL = 'https://api.infosimples.com/api/v2/consultas/sinesp/veiculo'
SINESP_LOGIN = "44954401879"
SINESP_PASSWORD = "Marley@gabi02"
SINESP_TOKEN = "VWgA6SlnN2ffE5d64JwlTuTf79uSVTWN9zw4PxU_"


def get_conexao():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD,
                            dsn=DB_DSN)


#passar placa do automóvel
def identificar_veiculo_api(placa):
    payload = {
        "placa": placa,
        "login_cpf": SINESP_LOGIN,
        "login_senha": SINESP_PASSWORD,
        "token": SINESP_TOKEN,
        "timeout": 300
    }

    response = requests.post(SINESP_URL, json=payload)
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