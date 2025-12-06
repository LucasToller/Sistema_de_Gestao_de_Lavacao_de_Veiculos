def input_int(msg):
    """Lê um inteiro do usuário, retornando None se estiver em branco."""
    while True:
        valor = input(msg)
        if valor.strip() == "":
            return None
        try:
            return int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")


def input_float(msg, allow_empty=True):
    """
    Lê um número decimal (float).
    Se allow_empty=True, ENTER vazio retorna None.
    Aceita vírgula ou ponto como separador.
    """
    while True:
        texto = input(msg).strip().replace(",", ".")
        if texto == "":
            if allow_empty:
                return None
            print("Este campo é obrigatório.")
            continue
        try:
            return float(texto)
        except ValueError:
            print("Digite um número válido (use ponto ou vírgula para decimais).")


def input_str(msg, required=False):
    """Lê uma string; se required=True, não permite vazio."""
    while True:
        s = input(msg).strip()
        if required and not s:
            print("Este campo é obrigatório.")
        else:
            return s


def pausar():
    input("\nPressione ENTER para continuar...")