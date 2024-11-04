
from api.banco import identificar_veiculo_api
from menuFeedbacks import menu_feedbacks
from menuOrcamentos import menu_orcamentos
from menuManutencao import menu_manutencao
from menuDiagnosticos import menu_diagnosticos
from menuAutomovel import menu_automoveis
from menuCliente import menu_clientes
from menuProblemas import menu_problemas


def menu_principal():
    while True:
        print("===== Menu Principal =====")
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Automóveis")
        print("3. Gerenciar Problemas")
        print("4. Gerenciar Diagnósticos")
        print("5. Gerenciar Manutenção")
        print("6. Gerenciar Orçamentos")
        print("7. Gerenciar Feedbacks")
        print("8. Consulta na API Sinesp")
        print("9. Sair")
        
        escolha = input("Escolha uma opção (1-8): ")

        if escolha == '1':
            menu_clientes()
        elif escolha == '2':
            menu_automoveis()
        elif escolha == '3':
            menu_problemas()
        elif escolha == '4':
            menu_diagnosticos()
        elif escolha == '5':
            menu_manutencao()
        elif escolha == '6':
            menu_orcamentos()()
        elif escolha == '7':
            menu_feedbacks()
        elif escolha == '8':
            placa = input("Digite a placa do veículo para consulta: ")
            try:
                dados_veiculo = identificar_veiculo_api(placa)
                print("===== Dados do Veículo =====")
                print(f"Modelo: {dados_veiculo.get('modelo')}")
                print(f"Marca: {dados_veiculo.get('marca')}")
                print(f"Ano: {dados_veiculo.get('ano')}")
                print(f"Cor: {dados_veiculo.get('cor')}")
                print(f"Placa: {dados_veiculo.get('placa')}")
            except Exception as e:
                print(f"Erro ao consultar veículo: {e}")
        elif escolha == '9':
            print("Saindo...")
            break

#Comentário: ao escolher a opção 8 do menu, o usuário consegur fazer um teste da api no sistema. Sem precisar apenas testar pelo endpoint criado.     


if __name__ == "__main__":
    menu_principal()