from flask import json
import oracledb



def menu_feedbacks():
    while True:
        print("\n===== Gerenciar Feedbacks =====")
        print("1. Criar Feedback")
        print("2. Listar Feedbacks")
        print("3. Atualizar Feedback")
        print("4. Excluir Feedback")
        print("5. Exportar Feedbacks para JSON")
        print("6. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção (1-6): ")

        if escolha == '1':
            criar_feedback()
        elif escolha == '2':
            listar_feedbacks()
        elif escolha == '3':
            atualizar_feedback()
        elif escolha == '4':
            excluir_feedback()
        elif escolha == '5':
            exportar_feedbacks_para_json()
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

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

def criar_feedback():
    conexao = get_conexao()
    cursor = conexao.cursor()

    comentario = input("Comentário avaliativo: ")
    pontuacao = int(input("Pontuação avaliativa: "))
    listar_ids_diagnostico()
    idDiagnostico = input("Informe o ID do diagnóstico da lista: ")

    sql= """INSERT INTO T_VB_FEEDBACK(id_feedback, ds_comentario_avaliativo, nr_pontuacao_avaliativa, id_diagnostico) VALUES (SQ_VB_FEEDBACK.NEXTVAL, :ds_comentario_avaliativo, :nr_pontuacao_avaliativa, :id_diagnostico)"""
    cursor.execute(sql, [comentario, pontuacao, idDiagnostico])
    conexao.commit()

    print("Feedback cadastrado com sucesso!")
    cursor.close()
    conexao.close()

def listar_feedbacks():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_FEEDBACK")

    feedbacks = cursor.fetchall()
    colunas = [col[0] for col in cursor.description]

    print("\n--- Lista de Feedbacks ---")
    for index, feedback in enumerate(feedbacks):
        print(f"{index + 1}. {dict(zip(colunas, feedback))}")

    cursor.close()
    conexao.close()

def escolher_feedback():
    listar_feedbacks()
    indice = int(input("Escolha o número do feedback: ")) -1
    return indice

def atualizar_feedback():
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    indice_feedback = escolher_feedback()
    cursor.execute("SELECT * FROM T_VB_FEEDBACK")
    feedback = cursor.fetchall()[indice_feedback]
    id_feedback = feedback[0]  # ID do cliente selecionado
    print(f"\nAtualizando feedback: {feedback}")

    print("Escolha o campo a ser atualizado:")
    print("1. Comentário avaliativo")
    print("2. Pontuação avaliativa")
    
    opcao = input("Opção: ")
    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "ds_comentario_avaliativo"
        novo_valor = input("Novo comentário: ")
    elif opcao == "2":
        campo = "nr_pontuacao_avaliativa"
        novo_valor = int(input("Nova pontuação: "))
    else:
        print("Opção inválida!")
        return
    
    sql = f"UPDATE T_VB_FEEDBACK SET {campo}=:novo_valor WHERE id_feedback=:id_feedback"
    cursor.execute(sql, {"novo_valor": novo_valor, "id_feedback": id_feedback})

    print("Feedback atualizado com sucesso!")
    cursor.close()
    conexao.close()

def excluir_feedback():
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    indice_feedback = escolher_feedback()
    cursor.execute("SELECT * FROM T_VB_FEEDBACK")
    feedback = cursor.fetchall()[indice_feedback]
    id_feedback = feedback[0]

    sql = "DELETE FROM T_VB_FEEDBACK WHERE id_feedback =:id_feedback"
    cursor.execute(sql, {"id_feedback": id_feedback})
    conexao.commit()

    print("Feedback excluído com sucesso!")
    cursor.close()
    conexao.close()

def exportar_feedbacks_para_json():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM T_VB_FEEDBACK")

    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor]

    with open("feedbacks.json", "w") as f:
        json.dump(dados, f, indent=4)

    print("Dados exportados para feedbacks.json")
    cursor.close()
    conexao.close()

