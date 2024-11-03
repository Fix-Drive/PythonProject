from flask import json
import oracledb



def menu_clientes():
    while True:
        print("\n===== Gerenciar Clientes =====")
        print("1. Criar Cliente")
        print("2. Listar Clientes")
        print("3. Atualizar Cliente")
        print("4. Excluir Cliente")
        print("5. Exportar Clientes para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_cliente()
        elif escolha == '2':
            listar_clientes()
        elif escolha == '3':
            atualizar_cliente()
        elif escolha == '4':
            excluir_cliente()
        elif escolha == '5':
            exportar_clientes_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

def get_conexao():
    return oracledb.connect(user="rm558830", password="070306",
                            dsn="oracle.fiap.com.br/orcl")

def criar_cliente():
    conexao = get_conexao()
    cursor = conexao.cursor()

    nome = input("Nome do Cliente: ")
    idade = int(input("Idade: "))
    email = input("E-mail: ")
    senha = input("Senha: ")
    cpf = int(input("CPF: "))
    rg = int(input("RG: "))
    endereco = input("Endereço: ")
    cnh = int(input("CNH: "))
    telefone = int(input("Telefone: "))

    sql = """
    INSERT INTO T_VB_CLIENTE (ID_CLIENTE, NM_CLIENTE, IDADE_CLIENTE, DS_EMAIL, DS_SENHA, NR_CPF, NR_RG, DS_ENDERECO, NR_CNH, NR_TELEFONE)
    VALUES (SQ_VB_CLIENTE.NEXTVAL, :nome, :idade, :email, :senha, :cpf, :rg, :endereco, :cnh, :telefone)
    """

    cursor.execute(sql, [nome, idade, email, senha, cpf, rg, endereco, cnh, telefone])
    conexao.commit()

    print("Cliente criado com sucesso!")
    cursor.close()
    conexao.close()

def listar_clientes():
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

def escolher_cliente():
    listar_clientes()
    indice = int(input("Escolha o número do cliente: ")) - 1
    return indice

def atualizar_cliente():
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    indice_cliente = escolher_cliente()
    cursor.execute("SELECT * FROM T_VB_CLIENTE")
    cliente = cursor.fetchall()[indice_cliente]
    id_cliente = cliente[0]  # ID do cliente selecionado
    print(f"\nAtualizando cliente: {cliente}")

    print("Escolha o campo a ser atualizado:")
    print("1. Nome")
    print("2. Idade")
    print("3. E-mail")
    print("4. Senha")
    print("5. Endereço")
    print("6. Telefone")
    
    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "NM_CLIENTE"
        novo_valor = input("Novo Nome: ")
    elif opcao == "2":
        campo = "IDADE_CLIENTE"
        novo_valor = int(input("Nova Idade: "))
    elif opcao == "3":
        campo = "DS_EMAIL"
        novo_valor = input("Novo E-mail: ")
    elif opcao == "4":
        campo = "DS_SENHA"
        novo_valor = input("Nova Senha: ")
    elif opcao == "5":
        campo = "DS_ENDERECO"
        novo_valor = input("Novo Endereço: ")
    elif opcao == "6":
        campo = "NR_TELEFONE"
        novo_valor = int(input("Novo Telefone: "))
    else:
        print("Opção inválida!")
        return
    
    sql = f"UPDATE T_VB_CLIENTE SET {campo} = :novo_valor WHERE ID_CLIENTE = :id_cliente"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_cliente": id_cliente})
    conexao.commit()

    print("Cliente atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_cliente():
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    indice_cliente = escolher_cliente()
    cursor.execute("SELECT * FROM T_VB_CLIENTE")
    cliente = cursor.fetchall()[indice_cliente]
    id_cliente = cliente[0]  # ID do cliente selecionado

    sql = "DELETE FROM T_VB_CLIENTE WHERE ID_CLIENTE = :id_cliente"
    cursor.execute(sql, {"id_cliente": id_cliente})
    conexao.commit()

    print("Cliente excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_clientes_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_CLIENTE")
    
    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("clientes.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para clientes.json")
    cursor.close()
    conexao.close()