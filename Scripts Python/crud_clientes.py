from datetime import date
from mysql.connector import Error

from db_config import get_connection
from utils import input_int, input_str, pausar


def listar_ids_clientes_resumido():
    """Mostra ID + nome de todos os clientes (para seleção em outros CRUDs)."""
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM cliente ORDER BY id;")
        rows = cur.fetchall()
        if rows:
            print("\n--- Clientes cadastrados ---")
            for r in rows:
                print(f"ID {r[0]} - {r[1]}")
        else:
            print("Nenhum cliente cadastrado.")
    except Error as e:
        print(f"Erro ao listar clientes: {e}")
    finally:
        cur.close()
        conn.close()


# CRUD CLIENTE
def criar_cliente():
    print("\n=== CADASTRAR CLIENTE ===")
    nome = input_str("Nome: ", required=True)
    cpf = input_str("CPF (opcional): ")
    email = input_str("E-mail (opcional): ")
    status = input_str("Status (ATIVO/INATIVO) [ATIVO]: ").upper() or "ATIVO"

    print("\n--- Dados do ENDEREÇO do cliente ---")
    logradouro = input_str("Logradouro: ", required=True)
    numero = input_str("Número: ", required=True)
    complemento = input_str("Complemento (opcional): ")
    bairro = input_str("Bairro: ", required=True)
    cidade = input_str("Cidade: ", required=True)
    cep = input_str("CEP: ", required=True)

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()

        sql_endereco = """
            INSERT INTO endereco (logradouro, numero, complemento, bairro, cidade, cep)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql_endereco, (logradouro, numero, complemento, bairro, cidade, cep))
        id_endereco = cur.lastrowid

        sql_cliente = """
            INSERT INTO cliente (nome, cpf, email, data_cadastro, status, id_endereco)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data_cadastro = date.today()
        cur.execute(sql_cliente, (nome, cpf, email, data_cadastro, status, id_endereco))

        conn.commit()
        print("\nCliente cadastrado com sucesso!")
    except Error as e:
        print(f"Erro ao cadastrar cliente: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def listar_clientes():
    print("\n=== LISTAR CLIENTES ===")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql = """
            SELECT c.id, c.nome, c.cpf, c.email, c.data_cadastro, c.status,
                   e.logradouro, e.numero, e.bairro, e.cidade, e.cep
            FROM cliente c
            JOIN endereco e ON c.id_endereco = e.id
            ORDER BY c.id;
        """
        cur.execute(sql)
        resultados = cur.fetchall()
        if not resultados:
            print("Nenhum cliente cadastrado.")
        else:
            for c in resultados:
                print(f"\nID: {c['id']} - {c['nome']} ({c['status']})")
                print(f"   CPF: {c['cpf']} | E-mail: {c['email']}")
                print(f"   Data cadastro: {c['data_cadastro']}")
                print(f"   Endereço: {c['logradouro']}, {c['numero']} - "
                      f"{c['bairro']} - {c['cidade']} - CEP:{c['cep']}")
    except Error as e:
        print(f"Erro ao listar clientes: {e}")
    finally:
        cur.close()
        conn.close()
        pausar()


def atualizar_cliente():
    print("\n=== ATUALIZAR CLIENTE ===")
    id_cliente = input_int("ID do cliente: ")
    if id_cliente is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql_sel = """
            SELECT c.*, e.logradouro, e.numero, e.complemento, e.bairro, e.cidade, e.cep
            FROM cliente c
            JOIN endereco e ON c.id_endereco = e.id
            WHERE c.id = %s
        """
        cur.execute(sql_sel, (id_cliente,))
        row = cur.fetchone()
        if not row:
            print("Cliente não encontrado.")
            return

        print(f"\nEditando cliente: {row['nome']} (ID {row['id']})")
        print("Deixe em branco para manter o valor atual.")

        nome = input(f"Nome [{row['nome']}]: ").strip() or row['nome']
        cpf = input(f"CPF [{row['cpf']}]: ").strip() or row['cpf']
        email = input(f"E-mail [{row['email']}]: ").strip() or row['email']
        status = input(f"Status [{row['status']}]: ").strip().upper() or row['status']

        logradouro = input(f"Logradouro [{row['logradouro']}]: ").strip() or row['logradouro']
        numero = input(f"Número [{row['numero']}]: ").strip() or row['numero']
        complemento = input(f"Complemento [{row['complemento']}]: ").strip() or row['complemento']
        bairro = input(f"Bairro [{row['bairro']}]: ").strip() or row['bairro']
        cidade = input(f"Cidade [{row['cidade']}]: ").strip() or row['cidade']
        cep = input(f"CEP [{row['cep']}]: ").strip() or row['cep']

        sql_up_end = """
            UPDATE endereco
            SET logradouro=%s, numero=%s, complemento=%s, bairro=%s, cidade=%s, cep=%s
            WHERE id = %s
        """
        cur.execute(sql_up_end, (logradouro, numero, complemento, bairro, cidade, cep,
                                 row['id_endereco']))

        sql_up_cli = """
            UPDATE cliente
            SET nome=%s, cpf=%s, email=%s, status=%s
            WHERE id = %s
        """
        cur.execute(sql_up_cli, (nome, cpf, email, status, id_cliente))

        conn.commit()
        print("\nCliente atualizado com sucesso!")
    except Error as e:
        print(f"Erro ao atualizar cliente: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def excluir_cliente():
    print("\n=== EXCLUIR CLIENTE ===")
    id_cliente = input_int("ID do cliente: ")
    if id_cliente is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        sql = "DELETE FROM cliente WHERE id = %s"
        cur.execute(sql, (id_cliente,))
        conn.commit()
        if cur.rowcount == 0:
            print("Cliente não encontrado.")
        else:
            print("Cliente excluído com sucesso!")
    except Error as e:
        print(f"Erro ao excluir cliente (possível vínculo com veículos/OS): {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def menu_clientes():
    while True:
        print("\n==== MENU CLIENTES ====")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("0 - Voltar")
        opc = input("Escolha: ")

        if opc == "1":
            criar_cliente()
        elif opc == "2":
            listar_clientes()
        elif opc == "3":
            atualizar_cliente()
        elif opc == "4":
            excluir_cliente()
        elif opc == "0":
            break
        else:
            print("Opção inválida.")