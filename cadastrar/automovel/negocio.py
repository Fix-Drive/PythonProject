
import  banco
def insere_automovel(dados_automovel, dados_api):
    dados = banco.consulta_automovel_placa(dados_automovel['placa_automovel'])
    if dados:
        raise Exception("Automóvel já existente")
    else:
        banco.insere_automovel(dados_automovel, dados_api)

def converte_automovel_dict(automovel: tuple) -> dict:
    return {"id_automovel": automovel[0], "placa_automovel": automovel[1], "ds_tipo_automovel": automovel[2], "ds_marca_automovel": automovel[3], "ds_modelo_automovel": automovel[4], "ds_porte_automovel": automovel[5], "ano_automovel": automovel[6], "cd_chassi": automovel[7], "cd_renavam": automovel[8], "id_cliente": automovel[9]}

def consulta_automoveis(id: int, placa:str, tipo_automovel:str, marca:str, modelo:str, porte_automovel:str, ano:int, cd_chassi:long, cd_renavam:long, id_cliente:int):
    if id:
        dado = banco.consulta_automovel_id(id)
        if dado:
            return converte_automovel_dict(dado)
    elif placa:
        dados = banco.consulta_automovel_placa(placa)
        resposta =[]
        for reg in dados:
            resposta.
    
    


def apaga_automovel(id:int):
    dados = banco.consulta_automovel_id(id)
    if not dados:
           raise ValueError("Automóvel não encontrado")
        
    banco.apagar_automovel(id)

       