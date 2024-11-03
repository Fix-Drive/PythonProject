from flask import json
import oracledb



def menu_orcamentos():
    while True:
        print("\n===== Gerenciar Orçamentos =====")
        print("1. Criar Orçamento")
        print("2. Listar Orçamentos")
        print("3. Atualizar Orçamento")
        print("4. Excluir Orçamento")
        print("5. Exportar Orçamentos para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_orcamento()
        elif escolha == '2':
            listar_orcamentos()
        elif escolha == '3':
            atualizar_orcamento()
        elif escolha == '4':
            excluir_orcamento()
        elif escolha == '5':
            exportar_orcamentos_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")
            return

def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

def listar_ids_manutencao():
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


def criar_orcamento():
    conexao = get_conexao()
    cursor = conexao.cursor()

    valorPeca = float(input("Valor da peça: "))
    valorServico = float(input("Valor do serviço: "))
    listar_ids_manutencao()
    idManutencao = input("Informe o ID da manutenção da lista: ")


    sql = """INSERT INTO T_VB_ORCAMENTO(id_orcamento, vl_peca, vl_servico, id_manutencao) VALUES (SQ_VB_ORCAMENTO.NEXTVAL, :vl_peca, :vl_servico, :id_manutencao)"""
    cursor.execute(sql, [valorPeca, valorServico, idManutencao])
    conexao.commit()

    print("Orçamento criado com sucesso!")
    cursor.close()
    conexao.close()

def listar_orcamentos():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_ORCAMENTO")

    orcamentos = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    print("\n--- Lista de Orçamentos ---")
    for index, orcamento in enumerate(orcamentos):
        print(f"{index + 1}. {dict(zip(colunas, orcamento))}")

    cursor.close()
    conexao.close()

def escolher_orcamento():
    listar_orcamentos()
    indice = int(input("Escolha o número do orçamento: ")) -1
    return indice

def atualizar_orcamento():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_orcamento = escolher_orcamento()
    cursor.execute("SELECT * FROM T_VB_ORCAMENTO")
    orcamento = cursor.fetchall()[indice_orcamento]
    id_orcamento = orcamento[0]
    print(f"\nAtualizando orçamento: {orcamento}")

    print("Escolha o campo a ser atualizado:")
    print("1. Valor da peça")
    print("2. Valor do serviço")

    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "vl_peca"
        novo_valor = float(input("Novo valor de peça: "))
    elif opcao == "2":
        campo = "vl_servico"
        novo_valor = float(input("Novo valor de serviço: "))
    else:
        print("Opção inválida!")
        return
    
    sql = f"UPDATE T_VB_ORCAMENTO SET {campo}=:novo_valor WHERE id_orcamento=:id_orcamento"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_orcamento":id_orcamento})
    conexao.commit()

    print("Orçamento atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_orcamento():
    conexao = get_conexao()
    cursor = conexao.cursor()

    indice_orcamento = escolher_orcamento()
    cursor.execute("SELECT * FROM T_VB_ORCAMENTO")
    orcamento = cursor.fetchall()[indice_orcamento]
    id_orcamento = orcamento[0]

    sql = "DELETE FROM T_VB_ORCAMENTO WHERE id_orcamento=:id_orcamento"
    cursor.execute(sql, {"id_orcamento": id_orcamento})
    conexao.commit()

    print("Orçamento excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_orcamentos_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_ORCAMENTO")
    
    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("orcamentos.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para orcamentos.json")
    cursor.close()
    conexao.close()

