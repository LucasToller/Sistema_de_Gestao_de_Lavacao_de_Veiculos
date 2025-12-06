from datetime import datetime
from mysql.connector import Error

from db_config import get_connection
from utils import input_int, input_float, pausar
from crud_clientes import listar_ids_clientes_resumido
from crud_veiculos import listar_veiculos_por_cliente_resumido


def criar_ordem_servico():
    print("\n=== ABRIR ORDEM DE SERVIÇO ===")
    print("\nSelecione o CLIENTE:")
    listar_ids_clientes_resumido()
    id_cliente = input_int("ID do cliente: ")
    if id_cliente is None:
        print("ID inválido.")
        pausar()
        return

    listar_veiculos_por_cliente_resumido(id_cliente)
    id_veiculo = input_int("ID do veículo: ")
    if id_veiculo is None:
        print("ID inválido.")
        pausar()
        return

    print("\nSelecione o FUNCIONÁRIO responsável:")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM funcionario ORDER BY id;")
        rows = cur.fetchall()
        if rows:
            for r in rows:
                print(f"ID {r[0]} - {r[1]}")
        else:
            print("Nenhum funcionário cadastrado.")
    except Error as e:
        print(f"Erro ao listar funcionários: {e}")
    finally:
        cur.close()
        conn.close()

    id_funcionario = input_int("ID do funcionário: ")
    if id_funcionario is None:
        print("ID inválido.")
        pausar()
        return

    observacoes = input("Observações (opcional): ").strip()
    valor_previsto = input_float("Valor total previsto (ex: 80,00) [opcional]: ", allow_empty=True)

    data_entrada = datetime.now()
    status = "ABERTA"

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO ordem_servico (
                data_hora_entrada, data_hora_saida, status, observacoes,
                valor_total_previsto, valor_total_final,
                id_cliente, id_veiculo, id_funcionario
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (
            data_entrada, None, status, observacoes,
            valor_previsto, None,
            id_cliente, id_veiculo, id_funcionario
        ))
        conn.commit()
        print("\nOrdem de serviço aberta com sucesso!")
    except Error as e:
        print(f"Erro ao abrir OS: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def listar_ordens_servico():
    print("\n=== LISTAR ORDENS DE SERVIÇO ===")
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql = """
            SELECT os.id, os.data_hora_entrada, os.data_hora_saida, os.status,
                   os.valor_total_previsto, os.valor_total_final,
                   c.nome  AS nome_cliente,
                   v.placa AS placa_veiculo,
                   v.modelo AS modelo_veiculo,
                   f.nome  AS nome_funcionario
            FROM ordem_servico os
            JOIN cliente    c ON os.id_cliente     = c.id
            JOIN veiculo    v ON os.id_veiculo     = v.id
            JOIN funcionario f ON os.id_funcionario = f.id
            ORDER BY os.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("Nenhuma ordem de serviço cadastrada.")
        else:
            for os in rows:
                print(f"\nOS {os['id']} - Status: {os['status']}")
                print(f"   Cliente: {os['nome_cliente']}")
                print(f"   Veículo: {os['modelo_veiculo']} ({os['placa_veiculo']})")
                print(f"   Funcionário: {os['nome_funcionario']}")
                print(f"   Entrada: {os['data_hora_entrada']}")
                print(f"   Saída:   {os['data_hora_saida']}")
                print(f"   Valor previsto: {os['valor_total_previsto']}")
                print(f"   Valor final:    {os['valor_total_final']}")
    except Error as e:
        print(f"Erro ao listar OS: {e}")
    finally:
        cur.close()
        conn.close()
        pausar()


def atualizar_ordem_servico():
    print("\n=== ATUALIZAR ORDEM DE SERVIÇO ===")
    id_os = input_int("ID da OS: ")
    if id_os is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        sql_sel = "SELECT * FROM ordem_servico WHERE id = %s"
        cur.execute(sql_sel, (id_os,))
        os = cur.fetchone()
        if not os:
            print("OS não encontrada.")
            return

        print(f"\nEditando OS {os['id']} - Status atual: {os['status']}")
        print("Deixe em branco para manter o valor atual.")

        status = input(f"Status [{os['status']}]: ").strip().upper() or os['status']
        observacoes = input(f"Observações [{os['observacoes']}]: ").strip() or os['observacoes']

        valor_prev = input_float(
            f"Valor previsto [{os['valor_total_previsto']}]: ",
            allow_empty=True
        )
        if valor_prev is None:
            valor_prev = os['valor_total_previsto']

        valor_final = input_float(
            f"Valor final [{os['valor_total_final']}]: ",
            allow_empty=True
        )
        if valor_final is None:
            valor_final = os['valor_total_final']

        if status == "CONCLUIDA" and os['data_hora_saida'] is None:
            data_saida = datetime.now()
        else:
            data_saida = os['data_hora_saida']

        sql_up = """
            UPDATE ordem_servico
            SET status=%s,
                observacoes=%s,
                valor_total_previsto=%s,
                valor_total_final=%s,
                data_hora_saida=%s
            WHERE id = %s
        """
        cur.execute(sql_up, (status, observacoes, valor_prev, valor_final, data_saida, id_os))
        conn.commit()
        print("\nOS atualizada com sucesso!")
    except Error as e:
        print(f"Erro ao atualizar OS: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def excluir_ordem_servico():
    print("\n=== EXCLUIR ORDEM DE SERVIÇO ===")
    id_os = input_int("ID da OS: ")
    if id_os is None:
        print("ID inválido.")
        pausar()
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        sql = "DELETE FROM ordem_servico WHERE id = %s"
        cur.execute(sql, (id_os,))
        conn.commit()
        if cur.rowcount == 0:
            print("OS não encontrada.")
        else:
            print("OS excluída com sucesso!")
    except Error as e:
        print(f"Erro ao excluir OS (possível vínculo com itens/pagamentos): {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        pausar()


def menu_ordens_servico():
    while True:
        print("\n==== MENU ORDEM DE SERVIÇO ====")
        print("1 - Abrir nova OS")
        print("2 - Listar OS")
        print("3 - Atualizar OS")
        print("4 - Excluir OS")
        print("0 - Voltar")
        opc = input("Escolha: ")

        if opc == "1":
            criar_ordem_servico()
        elif opc == "2":
            listar_ordens_servico()
        elif opc == "3":
            atualizar_ordem_servico()
        elif opc == "4":
            excluir_ordem_servico()
        elif opc == "0":
            break
        else:
            print("Opção inválida.")