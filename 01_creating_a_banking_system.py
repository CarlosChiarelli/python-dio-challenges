menu = """

[D] Deposit
[W] Withdraw
[S] Statement
[Q] Quit

=> """

balance = 0
limit = 500
statement = ""
withdrawal_count = 0
WITHDRAWAL_LIMIT = 3

while True:

    option = input(menu)

    if option == "D":
        amount = float(input("Enter the deposit amount: "))

        if amount > 0:
            balance += amount
            statement += f"Deposit: $ {amount:.2f}\n"
        else:
            print("Operation failed! The amount entered is invalid.")

    elif option == "W":
        amount = float(input("Enter the withdrawal amount: "))

        if amount <= 0:
            print("Operation failed! The amount entered is invalid.")
        elif amount > balance:
            print("Operation failed! You do not have enough balance.")
        elif amount > limit:
            print("Operation failed! The withdrawal amount exceeds the limit.")
        elif withdrawal_count >= WITHDRAWAL_LIMIT:
            print("Operation failed! Maximum number of withdrawals exceeded.")
        else:
            balance -= amount
            statement += f"Withdrawal: $ {amount:.2f}\n"
            withdrawal_count += 1

    elif option == "S":
        print("\n================ STATEMENT ================")
        if not statement:
            print("No transactions were made.")
        else:
            print(statement)
        print(f"\nBalance: $ {balance:.2f}")
        print("==========================================")

    elif option == "Q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")
