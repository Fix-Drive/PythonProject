from flask import json
import oracledb


def menu_automoveis():
    while True:
        print("\n===== Gerenciar Automóveis =====")
        print("1. Criar Automóvel")
        print("2. Listar Automóveis")
        print("3. Atualizar Automóvel")
        print("4. Excluir Automóvel")
        print("5. Exportar Automóveis para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_automoveis()
        elif escolha == '2':
            listar_automoveis()
        elif escolha == '3':
            atualizar_automovel()
        elif escolha == '4':
            excluir_automovel()
        elif escolha == '5':
            exportar_automoveis_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

def listar_ids_cliente():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_CLIENTE")
    
    clientes = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]
    
    print("\n--- Lista de Clientes ---")
    for index, cliente in enumerate(clientes):
        print(f"{index + 1}. {dict(zip(colunas, cliente))}")

    cursor.close()
    conexao.close()



def criar_automoveis():
    conexao = get_conexao()
    cursor = conexao.cursor()

    placa = input("Placa do automóvel: ")
    tipo = input("Tipo de automóvel: ")
    marca = input("Marca: ")
    modelo = input("Modelo")
    porte = input("Porte: ")
    ano = input("Ano de fabricação: ")
    chassi = input("Número de chassi: ")
    renavam = input("Código Renavam: ")
    listar_ids_cliente()
    idCliente = input("Informe o ID do cliente dono do automóvel: ")

    sql = """INSERT INTO T_VB_AUTOMOVEL(id_automovel, placa_automovel, ds_tipo_automovel, ds_marca_automovel, ds_modelo_automovel, ds_porte_automovel, ano_automovel, cd_chassi, cd_renavam, id_cliente) VALUES (SQ_VB_AUTOMOVEL.NEXTVAL, :placa_automovel, :ds_tipo_automovel, :ds_marca_automovel, :ds_modelo_automovel, :ds_porte_automovel, :ano_automovel, :cd_chassi, :cd_renavam, :id_cliente)"""

    cursor.execute(sql, [placa, tipo, marca, modelo, porte, ano, chassi, renavam, idCliente ])
    conexao.commit()
    
def listar_automoveis():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_AUTOMOVEL")

    automoveis = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    print("\n--- Lista de Automóveis ---")
    for index, automovel in enumerate(automoveis):
        print(f"{index + 1}. {dict(zip(colunas, automovel))}")
    
    cursor.close()
    conexao.close()

def escolher_automovel():
    listar_automoveis()
    indice = int(input("Escolha o número do automóvel: ")) - 1
    return indice

def atualizar_automovel():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_automovel = escolher_automovel()
    cursor.execute("SELECT * FROM T_VB_AUTOMOVEL")
    automovel = cursor.fetchall()[indice_automovel]
    id_automovel = automovel[0]
    print(f"\nAtualizando automóvel: {automovel}")

    print("Escolha o campo a ser atualizado:")
    print("1. Placa")
    print("2. Tipo")
    print("3. Marca")
    print("4. Modelo")
    print("5. Porte")
    print("6. Ano")
    print("7. Número Chassi")
    print("8. Código Renavam")

    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo == "placa_automovel"
        novo_valor == input("Nova placa: ")
    elif opcao == "2":
        campo = "ds_tipo_automovel"
        novo_valor = int(input("Novo tipo: "))
    elif opcao == "3":
        campo = "ds_marca_automovel"
        novo_valor = input("Nova marca: ")
    elif opcao == "4":
        campo = "ds_modelo_automovel"
        novo_valor = input("Novo modelo: ")
    elif opcao == "5":
        campo = "ds_porte_automovel"
        novo_valor = input("Novo porte: ")
    elif opcao == "6":
        campo = "ano_automovel"
        novo_valor = int(input("Novo ano: "))
    elif opcao == "7":
        campo == "cd_chassi"
        novo_valor == input("Novo número de chassi: ")
    elif opcao == "8":
        campo == "cd_renavam"
        novo_valor == int(input("Novo código renavam: "))
    else:
        print("Opção inválida!")
        
    sql = f"UPDATE T_VB_AUTOMOVEL SET {campo}=:novo_valor WHERE id_automovel =:id_automovel"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_automovel": id_automovel})
    conexao.commit()

    print("Automóvel atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_automovel():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_automovel = escolher_automovel()
    cursor.execute("SELECT * FROM T_VB_AUTOMOVEL")
    automovel = cursor.fetchall()[indice_automovel]
    id_automovel = automovel[0]

    sql = "DELETE FROM T_VB_AUTOMOVEL WHERE id_automovel=:id_automovel"
    cursor.execute(sql, {"id_automovel": id_automovel})
    conexao.commit()

    print("Automóvel excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_automoveis_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_AUTOMOVEL")

    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("automoveis.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para automoveis.json")
    cursor.close()
    conexao.close()



    