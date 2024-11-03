from flask import json
import oracledb



def menu_manutencao():
    while True:
        print("\n===== Gerenciar Manutenções =====")
        print("1. Criar Manutenção")
        print("2. Listar Manutenções")
        print("3. Atualizar Manutenção")
        print("4. Excluir Manutenção")
        print("5. Exportar Manutenções para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_manutencao()
        elif escolha == '2':
            listar_manutencoes()
        elif escolha == '3':
            atualizar_manutencao()
        elif escolha == '4':
            excluir_manutencao()
        elif escolha == '5':
            exportar_manutencoes_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")
            return

def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

def listar_ids_diagnostico():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_DIAGNOSTICO")

    diagnosticos = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    print("\n--- Lista de Diagnósticos ---")
    for index, diagnostico in enumerate(diagnosticos):
        print(f"{index + 1}. {dict(zip(colunas, diagnostico))}")

    cursor.close()
    conexao.close()

def listar_ids_problema():
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

def listar_ids_automovel():
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

def criar_manutencao():
    conexao = get_conexao()
    cursor = conexao.cursor()

    tipoManutencao = input("Tipo de manutenção: ")
    descricao = input("Descrição: ")
    pecaManutencao = input("Peça para manutenção: ")
    recomendacaoOficina = input("Recomendação de oficina: ")
    listar_ids_diagnostico()
    idDiagnostico = input("Informe o ID do diagnóstico da lista: ")
    listar_ids_problema()
    idProblema = input("Informe o ID do problema da lista: ")
    listar_ids_automovel()
    idAutomovel = input("Informe o ID do automóvel da lista: ")



    sql = """INSERT INTO T_VB_MANUTENCAO(id_manutencao, ds_tipo_manutencao, ds_descricao, ds_peca_manutencao, ds_recomendacao_oficina, id_diagnostico, id_problema, id_automovel) VALUES(SQ_VB_MANUTENCAO.NEXTVAL, :ds_tipo_manutencao, :ds_descricao, :ds_peca_manutencao, :ds_recomendacao_oficina, :id_diagnostico, :id_problema, :id_automovel) """
    cursor.execute(sql, [tipoManutencao, descricao, pecaManutencao, recomendacaoOficina, idDiagnostico, idProblema, idAutomovel])
    conexao.commit()

    print("Manutenção criada com sucesso!")
    cursor.close()
    conexao.close()

def listar_manutencoes():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_MANUTENCAO")

    manutencoes = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    
    print("\n--- Lista de Manutenções ---")
    for index, manutencao in enumerate(manutencoes):
        print(f"{index + 1}. {dict(zip(colunas, manutencao))}")

    cursor.close()
    conexao.close()

def escolher_manutencao():
    listar_manutencoes()
    indice = int(input("Escolha o número da manutenção: ")) -1
    return indice

def atualizar_manutencao():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_manutencao = escolher_manutencao()
    cursor.execute("SELECT * FROM T_VB_MANUTENCAO")
    manutencao = cursor.fetchall()[indice_manutencao]
    id_manutencao = manutencao[0]
    print(f"\nAtualizando a manutenção: {manutencao}")

    print("Escolha o campo a ser atualizado:")
    print("1. Tipo de manutenção")
    print("2. Descrição")
    print("3. Peça")
    print("4. Recomendação de oficina")

    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "ds_tipo_manutencao"
        novo_valor = input("Novo tipo: ")
    elif opcao == "2":
        campo = "ds_descricao"
        novo_valor = input("Nova descrição: ")
    elif opcao == "3":
        campo = "ds_peca_manutencao"
        novo_valor = input("Nova peça: ")
    elif opcao == "4":
        campo = "ds_recomendacao_oficina"
        novo_valor = input("Nova recomendação: ")
    else: 
        print("Opção inválida")
        return

    sql = f"UPDATE T_VB_MANUTENCAO SET {campo} =:novo_valor WHERE id_manutencao=:id_manutencao"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_manutencao": id_manutencao})
    conexao.commit()

def excluir_manutencao():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_manutencao = escolher_manutencao()
    cursor.execute("SELECT * FROM T_VB_MANUTENCAO")
    manutencao = cursor.fetchall()[indice_manutencao]
    id_manutencao = manutencao[0]

    sql = "DELETE FROM T_VB_MANUTENCAO WHERE id_manutencao=:id_manutencao"
    cursor.execute(sql, {"id_manutencao": id_manutencao})
    conexao.commit()

    print("Manutenção excluída com sucesso!")
    cursor.close()
    conexao.commit()

def exportar_manutencoes_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_MANUTENCAO")
    
    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("manutencoes.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para manutencoes.json")
    cursor.close()
    conexao.close()
