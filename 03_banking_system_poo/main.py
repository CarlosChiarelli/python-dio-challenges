import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(conta):
    valor = float(input("Informe o valor do depósito: "))
    conta.depositar(valor)


def sacar(conta):
    valor = float(input("Informe o valor do saque: "))
    conta.sacar(valor)


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['data']} - {transacao['transacao']}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_usuario(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_usuario(cpf, clientes)

    if cliente:
        numero_conta = len(contas) + 1
        conta = ContaCorrente(0, numero_conta, "0001", cliente, 500, 3)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                depositar(conta)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                sacar(conta)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                exibir_extrato(conta)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            criar_conta(clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
