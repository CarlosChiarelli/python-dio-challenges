from abc import ABC, abstractmethod
from datetime import datetime


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(self)
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f}"


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        excedeu_saldo = self.valor > conta.saldo
        excedeu_limite = self.valor > conta.limite
        excedeu_saques = conta.numero_saques >= conta.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            conta.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def __str__(self):
        return f"Saque: R$ {self.valor:.2f}"


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({"transacao": transacao, "data": datetime.now()})


class Conta:
    def __init__(self, saldo, numero, agencia, cliente, limite=500, limite_saques=3):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        self.limite = limite
        self.numero_saques = 0
        self.limite_saques = limite_saques

    def saldo(self):
        return self.saldo

    def nova_conta(cliente, numero):
        return Conta(0, numero, "0001", cliente)

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, limite, limite_saques):
        super().__init__(saldo, numero, agencia, cliente, limite, limite_saques)


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
