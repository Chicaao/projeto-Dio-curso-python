from datetime import date

class Transacao:
    def __init__(self, valor: float):
        self.valor = valor

    def descricao(self) -> str:
        raise NotImplementedError

class Deposito(Transacao):
    def descricao(self) -> str:
        return f"Depósito: R$ {self.valor:.2f}"

class Saque(Transacao):
    def descricao(self) -> str:
        return f"Saque: R$ {self.valor:.2f}"

class Historico:
    def __init__(self):
        self.transacoes: list[Transacao] = []

    def adicionar(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def gerar_extrato_texto(self) -> str:
        if not self.transacoes:
            return ""
        return "\n".join(t.descricao() for t in self.transacoes) + "\n"

class Cliente:
    def __init__(self, nome: str, endereco: str, cpf: str, data_nascimento: str):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.contas: list['Conta'] = []

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)

class Conta:
    def __init__(self, cliente: Cliente, numero: int, agencia: str):
        self.saldo: float = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar(Deposito(valor))
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def sacar(self, valor: float, limite: float, withdrawal_count: int, WITHDRAWAL_LIMIT: int):
        # Retorna (sucesso: bool, nova_withdrawal_count: int, mensagem já impressa)
        if valor > self.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False, withdrawal_count
        if valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False, withdrawal_count
        if withdrawal_count >= WITHDRAWAL_LIMIT:
            print("Operação falhou! Número máximo de saques diários excedido.")
            return False, withdrawal_count
        if valor > 0:
            self.saldo -= valor
            self.historico.adicionar(Saque(valor))
            withdrawal_count += 1
            print("Saque realizado com sucesso!")
            return True, withdrawal_count
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False, withdrawal_count

    def gerar_extrato(self) -> str:
        return self.historico.gerar_extrato_texto()

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, agencia: str, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

class SistemaBancario:
    def __init__(self):
        self.AGENCY = "0001"
        self.users: list[Cliente] = []
        self.accounts: list[Conta] = []
        self.next_account_number = 1
        # Defaults (mantidos do seu código original)
        self.WITHDRAWAL_LIMIT = 3

    def find_user_by_cpf(self, cpf: str):
        for u in self.users:
            if u.cpf == cpf:
                return u
        return None

    def find_account_by_number(self, number: int):
        for acc in self.accounts:
            if acc.numero == number:
                return acc
        return None

    def create_user(self):
        cpf = input("Informe o CPF (somente números): ").strip()
        if self.find_user_by_cpf(cpf):
            print("Já existe usuário com esse CPF!")
            return

        name = input("Informe o nome completo: ").strip()
        birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
        address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

        novo = Cliente(nome=name, endereco=address, cpf=cpf, data_nascimento=birth_date)
        self.users.append(novo)
        print("Usuário criado com sucesso!")

    def create_account(self):
        cpf = input("Informe o CPF do usuário: ").strip()
        user = self.find_user_by_cpf(cpf)

        if user:
            acc_number = self.next_account_number
            conta = ContaCorrente(cliente=user, numero=acc_number, agencia=self.AGENCY)
            user.adicionar_conta(conta)
            self.accounts.append(conta)
            self.next_account_number += 1

            print("\n=== Conta criada com sucesso! ===")
            print(f"Agência: {self.AGENCY}")
            print(f"Número da conta: {acc_number}")
            print(f"Titular: {user.nome}")
            return
        else:
            print("Usuário não encontrado, fluxo de criação de conta encerrado!")
            return

    def access_account(self):
        if not self.accounts:
            print("Nenhuma conta cadastrada! Por favor, crie uma conta primeiro.")
            return

        try:
            account_number = int(input("Informe o número da conta: ").strip())
        except ValueError:
            print("Número de conta inválido!")
            return

        selected_account = self.find_account_by_number(account_number)
        if not selected_account:
            print("Conta não encontrada!")
            return

        print(f"\n=== Acessando a conta {account_number} ===")
        # mantenho os limites por sessão (como no seu código anterior)
        limit = getattr(selected_account, "limite", 500.0)
        withdrawal_count = 0  # reset por sessão (o procedural fazia isso globalmente)
        menu = """\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

    => """

        while True:
            option = input(menu).strip()

            if option == "1":
                try:
                    amount = float(input("Informe o valor do depósito: ").strip())
                except ValueError:
                    print("Valor inválido.")
                    continue
                selected_account.depositar(amount)

            elif option == "2":
                try:
                    amount = float(input("Informe o valor do saque: ").strip())
                except ValueError:
                    print("Valor inválido.")
                    continue

                success, withdrawal_count = selected_account.sacar(
                    valor=amount,
                    limite=limit,
                    withdrawal_count=withdrawal_count,
                    WITHDRAWAL_LIMIT=self.WITHDRAWAL_LIMIT
                )
                # já imprime mensagens dentro do método sacar

            elif option == "3":
                print("\n================ EXTRATO ================")
                extrato_texto = selected_account.gerar_extrato()
                print("Não foram realizadas movimentações." if not extrato_texto else extrato_texto)
                print(f"\nSaldo: R$ {selected_account.saldo:.2f}")
                print("=========================================")

            elif option == "4":
                print("Saindo da conta. Até logo!")
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

    def run(self):
        while True:
            print("\n=== Bem vindo ao Banco ===")
            option = input("Selecione uma opção:\n[1] Criar usuário\n[2] Criar conta\n[3] Acessar conta\n[4] Sair\n=> ").strip()

            if option == "1":
                self.create_user()
            elif option == "2":
                self.create_account()
            elif option == "3":
                self.access_account()
            elif option == "4":
                print("Saindo do sistema. Até logo!")
                break
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    sistema = SistemaBancario()
    sistema.run()