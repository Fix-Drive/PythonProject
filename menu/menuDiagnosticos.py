from flask import json
import oracledb


def menu_diagnosticos():
    while True:
        print("\n===== Gerenciar Diagnósticos =====")
        print("1. Criar Diagnóstico")
        print("2. Listar Diagnósticos")
        print("3. Atualizar Diagnóstico")
        print("4. Excluir Diagnóstico")
        print("5. Exportar Diagnóstico para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_diagnostico()
        elif escolha == '2':
            listar_diagnosticos()
        elif escolha == '3':
            atualizar_diagnostico()
        elif escolha == '4':
            excluir_diagnostico()
        elif escolha == '5':
            exportar_diagnosticos_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")
            return

def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

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

def criar_diagnostico():
    conexao = get_conexao()
    cursor = conexao.cursor()

    resultadoDiagnostico = input("Resultado diagnóstico: ")
    listar_ids_problema()
    idProblema = input("Informe o ID do problema: ")
    listar_ids_automovel()
    idAutomovel = input("Informe o ID do automóvel: ")


    sql = """INSERT INTO T_VB_DIAGNOSTICO(id_diagnostico, ds_resultado_diagnostico, id_problema, id_automovel) VALUES (SQ_VB_DIAGNOSTICO.NEXTVAL, :ds_resultado_diagnostico, :id_problema, :id_automovel)"""

    cursor.execute(sql, [resultadoDiagnostico, idProblema, idAutomovel])
    conexao.commit()

    print("Diagnóstico criado com sucesso!")
    cursor.close()
    conexao.close()

def listar_diagnosticos():
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

def escolher_diagnostico():
    listar_diagnosticos()
    indice = int(input("Escolha o número do diagnóstico: ")) -1
    return indice

def atualizar_diagnostico():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_diagnostico = escolher_diagnostico()
    cursor.execute("SELECT * FROM T_VB_DIAGNOSTICO")
    diagnostico = cursor.fetchal()[indice_diagnostico]
    id_diagnostico = diagnostico[0]
    print(f"\nAtualizando diagnóstico: {diagnostico}")

    print("O campo a ser atualizado será:")
    print("1. Resultado diagnóstico")

    opcao = 1
    campo = None
    novo_valor = None

    campo = "ds_resultado_diagnostico"
    novo_valor = input("Novo resultado: ")

    sql= f"UPDATE T_VB_DIAGNOSTICO SET {campo} =:novo_valor WHERE id_diagnostico=:id_diagnostico"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_diagnostico": id_diagnostico})
    conexao.commit()

    print("Diagnóstico atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_diagnostico():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_diagnostico = escolher_diagnostico()
    cursor.execute("SELECT * FROM T_VB_DIAGNOSTICO")
    diagnostico = cursor.fetchall()[indice_diagnostico]
    id_diagnostico = diagnostico[0]

    sql = "DELETE FROM T_VB_DIAGNOSTICO WHERE id_diagnostico=:id_diagnostico"
    cursor.execute(sql, {"id_diagnostico": id_diagnostico})
    conexao.commit()

    print("Diagnóstico excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_diagnosticos_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_DIAGNOSTICO")

    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("diagnosticos.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para diagnosticos.json")
    cursor.close()
    conexao.close()