def withdraw(*, balance, amount, statement, limit, withdrawals_count, max_withdrawals):
    if amount > balance:
        print("Operation failed! Insufficient balance.")
    elif amount > limit:
        print("Operation failed! Withdrawal amount exceeds limit.")
    elif withdrawals_count >= max_withdrawals:
        print("Operation failed! Maximum number of withdrawals exceeded.")
    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal: ${amount:.2f}\n"
        withdrawals_count += 1
        print("Withdrawal successful!")
    else:
        print("Operation failed! Invalid amount.")
    return balance, statement, withdrawals_count


def deposit(balance, amount, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Deposit: ${amount:.2f}\n"
        print("Deposit successful!")
    else:
        print("Operation failed! Invalid amount.")
    return balance, statement


def bank_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions made." if not statement else statement)
    print(f"\nBalance: ${balance:.2f}")
    print("==========================================")


def register_user(users):
    name = input("Enter name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    cpf = input("Enter CPF (only numbers): ")
    address = input("Enter address (street, number - neighborhood - city/state): ")

    if any(user["cpf"] == cpf for user in users):
        print("A user with this CPF already exists!")
    else:
        users.append(
            {"name": name, "birth_date": birth_date, "cpf": cpf, "address": address}
        )
        print("User registered successfully!")


def register_account(accounts, users):
    cpf = input("Enter the user's CPF: ")
    user = next((user for user in users if user["cpf"] == cpf), None)

    if user:
        user_accounts = [account for account in accounts if account["user"]["cpf"] == cpf]
        account_number = len(user_accounts) + 1
        accounts.append(
            {"agency": "0001", "account_number": account_number, "user": user}
        )
        print("Account registered successfully!")
    else:
        print("User not found! Account registration failed.")


# Variable initialization
balance = 0
limit = 500
statement = ""
withdrawals_count = 0
MAX_WITHDRAWALS = 3

users = []
accounts = []

menu = """
[d] Deposit
[w] Withdraw
[s] Statement
[u] Register User
[a] Register Account
[q] Quit

=> """

while True:
    option = input(menu)

    if option == "d":
        amount = float(input("Enter the deposit amount: "))
        balance, statement = deposit(balance, amount, statement)

    elif option == "w":
        amount = float(input("Enter the withdrawal amount: "))
        balance, statement, withdrawals_count = withdraw(
            balance=balance,
            amount=amount,
            statement=statement,
            limit=limit,
            withdrawals_count=withdrawals_count,
            max_withdrawals=MAX_WITHDRAWALS,
        )

    elif option == "s":
        bank_statement(balance, statement=statement)

    elif option == "u":
        register_user(users)

    elif option == "a":
        register_account(accounts, users)

    elif option == "q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")
