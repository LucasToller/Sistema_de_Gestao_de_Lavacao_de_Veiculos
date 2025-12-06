from mysql.connector import Error

from db_config import get_connection
from utils import input_int, input_str, pausar
from crud_clientes import listar_ids_clientes_resumido


def criar_veiculo():
    print("\n=== CADASTRAR VEÍCULO ===")
    marca = input_str("Marca (opcional): ")
    modelo = input_str("Modelo: ", required=True)
    ano = input_int("Ano (opcional): ")
    cor = input_str("Cor (opcional): ")
    placa = input_str("Placa: ", required=True).upper()
    tipo = input_str("Tipo (Carro/Moto/etc, opcional): ")

    print("\nInforme o ID do cliente dono do veículo.")
    listar_ids_clientes_resumido()

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
        sql = """
            INSERT INTO veiculo (marca, modelo, ano, cor, placa, tipo, id_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (marca, modelo, ano, cor, placa, tipo, id_cliente))
        conn.commit()
        print("\nVeículo cadastrado com sucesso!")
    except Error as e:
        print(f"Erro ao cadastrar veículo: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def listar_veiculos():
    print("\n=== LISTAR VEÍCULOS ===")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql = """
            SELECT v.id, v.marca, v.modelo, v.ano, v.cor, v.placa, v.tipo,
                   c.nome AS nome_cliente
            FROM veiculo v
            JOIN cliente c ON v.id_cliente = c.id
            ORDER BY v.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("Nenhum veículo cadastrado.")
        else:
            for v in rows:
                print(f"\nID: {v['id']} - {v['marca']} {v['modelo']} ({v['placa']})")
                print(f"   Ano: {v['ano']} | Cor: {v['cor']} | Tipo: {v['tipo']}")
                print(f"   Cliente: {v['nome_cliente']}")
    except Error as e:
        print(f"Erro ao listar veículos: {e}")
    finally:
        cur.close()
        conn.close()
        pausar()


def listar_veiculos_por_cliente_resumido(id_cliente):
    """Auxiliar para OS: lista veículos de um cliente."""
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, modelo, placa FROM veiculo WHERE id_cliente = %s",
            (id_cliente,)
        )
        rows = cur.fetchall()
        if rows:
            print("\n--- Veículos do cliente ---")
            for r in rows:
                print(f"ID {r[0]} - {r[1]} ({r[2]})")
        else:
            print("Nenhum veículo cadastrado para esse cliente.")
    except Error as e:
        print(f"Erro ao listar veículos do cliente: {e}")
    finally:
        cur.close()
        conn.close()


def atualizar_veiculo():
    print("\n=== ATUALIZAR VEÍCULO ===")
    id_veiculo = input_int("ID do veículo: ")
    if id_veiculo is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql_sel = "SELECT * FROM veiculo WHERE id = %s"
        cur.execute(sql_sel, (id_veiculo,))
        v = cur.fetchone()
        if not v:
            print("Veículo não encontrado.")
            return

        print(f"\nEditando veículo ID {v['id']} - {v['modelo']} ({v['placa']})")
        print("Deixe em branco para manter o valor atual.")

        marca = input(f"Marca [{v['marca']}]: ").strip() or v['marca']
        modelo = input(f"Modelo [{v['modelo']}]: ").strip() or v['modelo']
        ano_str = input(f"Ano [{v['ano']}]: ").strip()
        ano = v['ano']
        if ano_str != "":
            try:
                ano = int(ano_str)
            except ValueError:
                print("Ano inválido. Mantendo valor anterior.")
        cor = input(f"Cor [{v['cor']}]: ").strip() or v['cor']
        placa = input(f"Placa [{v['placa']}]: ").strip().upper() or v['placa']
        tipo = input(f"Tipo [{v['tipo']}]: ").strip() or v['tipo']

        sql_up = """
            UPDATE veiculo
            SET marca=%s, modelo=%s, ano=%s, cor=%s, placa=%s, tipo=%s
            WHERE id = %s
        """
        cur.execute(sql_up, (marca, modelo, ano, cor, placa, tipo, id_veiculo))
        conn.commit()
        print("\nVeículo atualizado com sucesso!")
    except Error as e:
        print(f"Erro ao atualizar veículo: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def excluir_veiculo():
    print("\n=== EXCLUIR VEÍCULO ===")
    id_veiculo = input_int("ID do veículo: ")
    if id_veiculo is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        sql = "DELETE FROM veiculo WHERE id = %s"
        cur.execute(sql, (id_veiculo,))
        conn.commit()
        if cur.rowcount == 0:
            print("Veículo não encontrado.")
        else:
            print("Veículo excluído com sucesso!")
    except Error as e:
        print(f"Erro ao excluir veículo (possível vínculo com OS): {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def menu_veiculos():
    while True:
        print("\n==== MENU VEÍCULOS ====")
        print("1 - Cadastrar veículo")
        print("2 - Listar veículos")
        print("3 - Atualizar veículo")
        print("4 - Excluir veículo")
        print("0 - Voltar")
        opc = input("Escolha: ")

        if opc == "1":
            criar_veiculo()
        elif opc == "2":
            listar_veiculos()
        elif opc == "3":
            atualizar_veiculo()
        elif opc == "4":
            excluir_veiculo()
        elif opc == "0":
            break
        else:
            print("Opção inválida.")