"""
UNIVALI - Banco de Dados - M3
Parte 2: CRUDs com persistência em MySQL

Tabelas cobertas:
- cliente
- veiculo
- ordem_servico
"""

from crud_clientes import menu_clientes
from crud_veiculos import menu_veiculos
from crud_ordens_servico import menu_ordens_servico

def menu_principal():
    while True:
        print("\n==============================")
        print("  SISTEMA LAVAÇÃO - M3 BD")
        print("==============================")
        print("1 - CRUD Clientes")
        print("2 - CRUD Veículos")
        print("3 - CRUD Ordens de Serviço")
        print("0 - Sair")
        opc = input("Escolha: ")

        if opc == "1":
            menu_clientes()
        elif opc == "2":
            menu_veiculos()
        elif opc == "3":
            menu_ordens_servico()
        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()