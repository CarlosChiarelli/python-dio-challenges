def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques


def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def extrato_bancario(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def cadastrar_usuario(usuarios):
    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    cpf = input("Informe o CPF (somente números): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )

    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("Já existe um usuário com esse CPF!")
    else:
        usuarios.append(
            {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "cpf": cpf,
                "endereco": endereco,
            }
        )
        print("Usuário cadastrado com sucesso!")


def cadastrar_conta(contas, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

    if usuario:
        contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
        numero_conta = len(contas_usuario) + 1
        contas.append(
            {"agencia": "0001", "numero_conta": numero_conta, "usuario": usuario}
        )
        print("Conta cadastrada com sucesso!")
    else:
        print("Usuário não encontrado! Cadastro de conta não realizado.")


# Inicialização de variáveis
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

usuarios = []
contas = []

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar Usuário
[c] Cadastrar Conta
[q] Sair

=> """

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )

    elif opcao == "e":
        extrato_bancario(saldo, extrato=extrato)

    elif opcao == "u":
        cadastrar_usuario(usuarios)

    elif opcao == "c":
        cadastrar_conta(contas, usuarios)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
