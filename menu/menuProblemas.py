from flask import json
import oracledb


def menu_problemas():
    while True:
        print("\n===== Gerenciar Problemas =====")
        print("1. Criar Problemas")
        print("2. Listar Problemas")
        print("3. Atualizar Problema")
        print("4. Excluir Problema")
        print("5. Exportar Problemas para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_problema()
        elif escolha == '2':
            listar_problemas()
        elif escolha == '3':
            atualizar_problema()
        elif escolha == '4':
            excluir_problema()
        elif escolha == '5':
            exportar_problemas_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")


def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

def listar_ids_automoveis():
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

def criar_problema():
    conexao = get_conexao()
    cursor = conexao.cursor()

    tipoProblema = input("Tipo de problema: ")
    descricao = input("Descrição: ")
    pontuacaGravidade = int(input("Pontuação de gravidade: "))
    listar_ids_automoveis()
    idAutomovel = input("Informe o ID do automóvel: ")

    sql = """INSERT INTO T_VB_PROBLEMA(id_problema, ds_tipo_problema, ds_descricao, nr_pontuacao_gravidade, id_automovel) VALUES (SQ_VB_PROBLEMA.NEXTVAL, :ds_tipo_problema, :ds_descricao, :nr_pontuacao_gravidade, :id_automovel)"""
    cursor.execute(sql, [tipoProblema, descricao, pontuacaGravidade, idAutomovel])
    conexao.commit()

    print("Problema criado com sucesso!")
    cursor.close()
    conexao.close()

def listar_problemas():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_PROBLEMA")

    problemas = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    print("\n--- Lista de Problemas ---")
    for index, problema in enumerate(problemas):
        print(f"{index + 1}. {dict(zip(colunas, problema))}")

    cursor.close()
    conexao.close()

def escolher_problema():
    listar_problemas()
    indice = int(input("Escolha o número do problema: ")) - 1
    return indice

def atualizar_problema():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_problema = escolher_problema()
    cursor.execute("SELECT * FROM T_VB_PROBLEMA")
    problema = cursor.fetchall()[indice_problema]
    id_problema = problema[0]
    print(f"\nAtualizando problema: {problema}")

    print("Escolha o campo a ser atualizado:")
    print("1. Tipo problema")
    print("2. Descrição")
    print("3. Pontuação")
    
    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "ds_tipo_problema"
        novo_valor = input("Novo tipo: ")
    elif opcao == "2":
        campo = "ds_descricao"
        novo_valor = input("Nova descrição: ")
    elif opcao == "3":
        campo = "nr_pontuacao_gravidade"
        novo_valor = int(input("Nova pontuação: "))
    else:
        print("Opção inválida!")

    sql = f"UPDATE T_VB_PROBLEMA SET {campo}=: novo_valor WHERE id_problema=:id_problema"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_problema": id_problema})
    conexao.commit()

    print("Problema atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_problema():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_problema = escolher_problema()
    cursor.execute("SELECT * FROM T_VB_PROBLEMA")
    problema = cursor.fetchall()[indice_problema]
    id_problema = problema[0]

    sql = "DELETE FROM T_VB_PROBLEMA WHERE id_problema = :id_problema"
    cursor.execute(sql, {"id_problema": id_problema})
    conexao.commit()

    print("Problema excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_problemas_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_PROBLEMA")

    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("problemas.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para problemas.json")
    cursor.close()
    conexao.close()