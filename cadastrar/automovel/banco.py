from matplotlib.pyplot import get
from numpy import long
import oracledb
import api.configurations as configurations
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
    

def insere_automovel(dados_automovel, dados_api):
    sql = "insert into t_vb_automovel(placa_automovel, ds_tipo_automovel, ds_marca_automovel, ds_modelo_automovel, ds_porte_automovel, ano_automovel, cd_chassi, cd_renavam, id_cliente) VALUES (:placa_automovel, :ds_tipo_automovel, :ds_marca_automovel, :ds_modelo_automovel, :ds_porte_automovel, :ano_automovel, :cd_chassi, :cd_renavam, :id_cliente) RETURNING id_automovel"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {
                "placa_automovel": dados_automovel["placa"],
                "ds_tipo_automovel": dados_automovel["tipo_automovel"],
                "ds_marca_automovel": dados_api["marca"],
                "ds_modelo_automovel": dados_api["modelo"],
                "ds_porte_automovel": dados_automovel["porte_automovel"],
                "ano_automovel": dados_api["ano"],
                "cd_chassi": dados_automovel["cd_chassi"],
                "cd_renavam": dados_automovel["cd_renavam"],
                "id_cliente": dados_automovel["id_cliente"]
            })

        con.commit()
        return "Automóvel cadastrado com sucesso"
    
def consulta_automovel_id(id:int):
    sql = "select id_automovel, placa_automovel, ds_tipo_automovel, ds_marca_automovel, ds_modelo_automovel, ds_porte_automovel, ano_automovel, cd_chassi, cd_renavam from t_vb_automovel where id_automovel=:id_automovel"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id_automovel": id})
            return cur.fetchone()


def update_automovel(automovel:dict):
    sql = "update t_vb_automovel set placa_automovel=:placa_automovel, ds_tipo_automovel=:ds_tipo_automovel, ds_marca_automovel=:ds_marca_automovel, ds_modelo_automovel=:ds_modelo_automovel, ds_porte_automovel=:ds_porte_automovel, ano_automovel=:ano_automovel, cd_chassi=:cd_chassi, cd_renavam=:cd_renavam, id_cliente=:id_cliente"
    with get_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, automovel)
        conn.commit()

def apagar_automovel(id:int):
    sql = "delete from t_vb_automovel where id_automovel=:id_automovel"
    with get_conexao() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"id_automovel": id})
        conn.commit()

def consulta_automovel_placa(placa:str):
    sql = "select id_automovel, placa_automovel, ds_tipo_automovel, ds_marca_automovel, ds_modelo_automovel, ds_porte_automovel, ano_automovel, cd_chassi, cd_renavam, id_cliente from t_vb_automovel where placa_automovel=:placa_automovel"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"placa_automovel":{placa} })
            return cur.fetchall()