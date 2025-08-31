def filter_user (cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None

def create_user (users):
    cpf = input("Informe o CPF (somente números): ")
    user = filter_user(cpf, users)

    if user:
        print("Já existe usuário com esse CPF!")
        return
    
    name = input("Informe o nome completo: ")
    birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
    address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    users.append({"nome": name, "data_nascimento": birth_date, "cpf": cpf, "endereco": address})

    print("Usuário criado com sucesso!")
    
def create_account (agency, account_number, users, accounts):
    cpf = input("Informe o CPF do usuário: ")
    user = filter_user(cpf, users)

    if user:
        print("\n=== Conta criada com sucesso! ===")
        print(f"Agência: {agency}")
        print(f"Número da conta: {account_number}")
        print(f"Titular: {user['nome']}")
        
        accounts.append({"agencia": agency, "numero_conta": account_number, "usuario": user, "balance": 0, "statement": "", "withdrawal_count": 0})
        return account_number + 1
    else:
        print("Usuário não encontrado, fluxo de criação de conta encerrado!")
        return account_number

def deposit (amount, balance, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Depósito: R$ {amount:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:   
        print("Operação falhou! O valor informado é inválido.")
    
    return balance, statement

def withdraw (*, amount, balance, statement, withdrawal_count, limit, WITHDRAWAL_LIMIT):
    exceeded_balance = amount > balance

    exceeded_limit = amount > limit

    exceeded_withdrawals = withdrawal_count >= WITHDRAWAL_LIMIT

    if exceeded_balance:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif exceeded_limit:
        print("Operação falhou! O valor do saque excede o limite.")

    elif exceeded_withdrawals:
        print("Operação falhou! Número máximo de saques diários excedido.")

    elif amount > 0:
        balance -= amount
        statement += f"Saque: R$ {amount:.2f}\n"
        withdrawal_count += 1
        print("Saque realizado com sucesso!")

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return balance, statement, withdrawal_count

def display_statement (balance, /, *, statement, ):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not statement else statement)
    print(f"\nSaldo: R$ {balance:.2f}") 
    print("=========================================")

def main():
    AGENCY = "0001"
    balance = 0
    limit = 500
    statement = ""
    withdrawal_count = 0
    WITHDRAWAL_LIMIT = 3
    users = []
    accounts = []
    next_account_number = 1
    menu = """\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

    => """

    while True:
        print("\n=== Bem vindo ao Banco ===")
        option = input("Selecione uma opção:\n[1] Criar usuário\n[2] Criar conta\n[3] Acessar conta\n[4] Sair\n=> ")

        if option == "1":
            create_user(users)
            
        elif option == "2":
            next_account_number = create_account(AGENCY, next_account_number, users, accounts)
            
        elif option == "3":
            if not accounts:
                print("Nenhuma conta cadastrada! Por favor, crie uma conta primeiro.")
                continue

            account_number = int(input("Informe o número da conta: "))
            account = [acc for acc in accounts if acc["numero_conta"] == account_number]

            if not account:
                print("Conta não encontrada!")
                continue

            selected_account = account[0]
            print(f"\n=== Acessando a conta {account_number} ===")
        
            while True:
                option = input(menu)

                if option == "1":
                    amount = float(input("Informe o valor do depósito: "))
                    balance_of_account = selected_account['balance']
                    statement_of_account = selected_account['statement']

                    new_balance, new_statement = deposit(amount, balance_of_account, statement_of_account)

                    selected_account['balance'] = new_balance
                    selected_account['statement'] = new_statement

                elif option == "2":
                    amount = float(input("Informe o valor do saque: "))
    
                    # Chama a função withdraw, passando todos os dados necessários
                    new_balance, new_statement, new_withdrawal_count = withdraw(
                        amount=amount,
                        balance=selected_account['balance'],
                        statement=selected_account['statement'],
                        withdrawal_count=selected_account['withdrawal_count'],
                        limit=limit,
                        WITHDRAWAL_LIMIT=WITHDRAWAL_LIMIT
                    )
    
                    # Atualiza todos os dados na conta selecionada
                    selected_account['balance'] = new_balance
                    selected_account['statement'] = new_statement
                    selected_account['withdrawal_count'] = new_withdrawal_count

                elif option == "3":
                    # Chama a função statement com os dados da conta selecionada
                    display_statement(selected_account['balance'], statement=selected_account['statement'])

                elif option == "4":
                    print("Saindo da conta. Até logo!")
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")

        elif option == "4":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
    
