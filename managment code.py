
import tkinter as tk
from tkinter import messagebox

class Transaction:
    def __init__(self, type, amount, balance):
        self.type = type
        self.amount = amount
        self.balance = balance

    def __str__(self):
        return f"{self.type}: {self.amount}, Balance after transaction: {self.balance}"

class Account:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(Transaction("Deposit", amount, self.balance))
            return f"Deposited {amount}. New balance is {self.balance}."
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(Transaction("Withdraw", amount, self.balance))
            return f"Withdrew {amount}. New balance is {self.balance}."
        else:
            return "Invalid withdraw amount or insufficient balance."
 
    def transfer(self, amount, recipient_account):
        if 0 < amount <= self.balance:
            self.balance -= amount
            recipient_account.balance += amount
            self.transactions.append(Transaction("Transfer Out", amount, self.balance))
            recipient_account.transactions.append(Transaction("Transfer In", amount, recipient_account.balance))
            return f"Transferred {amount} to account {recipient_account.account_number}. New balance is {self.balance}."
        else:
            return "Invalid transfer amount or insufficient balance."

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

    def __str__(self):
        return f"Account[{self.account_number}]: {self.account_holder}, Balance: {self.balance}"

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, account_number, account_holder):
        if account_number in self.accounts:
            return "Account number already exists."
        else:
            self.accounts[account_number] = Account(account_number, account_holder)
            return f"Account created for {account_holder} with account number {account_number}."

    def get_account(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            return None

    def deposit_to_account(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            return account.deposit(amount)
        else:
            return "Account not found."

    def withdraw_from_account(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            return account.withdraw(amount)
        else:
            return "Account not found."

    def transfer_between_accounts(self, from_account_number, to_account_number, amount):
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)
        if from_account and to_account:
            return from_account.transfer(amount, to_account)
        else:
            return "One or both accounts not found."

    def __str__(self):
        accounts_summary = "\n".join([str(account) for account in self.accounts.values()])
        return f"Bank: {self.name}\nAccounts:\n{accounts_summary}"

class BankApp:
    def __init__(self, root):
        self.bank = Bank("My Bank")
        self.root = root
        self.root.title("Bank Management System")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.main_frame, text="Bank Management System", font=("Helvetica", 16)).grid(row=0, columnspan=2)

        tk.Button(self.main_frame, text="Create Account", command=self.create_account_window).grid(row=1, column=0, pady=10)
        tk.Button(self.main_frame, text="Deposit Money", command=self.deposit_window).grid(row=1, column=1, pady=10)
        tk.Button(self.main_frame, text="Withdraw Money", command=self.withdraw_window).grid(row=2, column=0, pady=10)
        tk.Button(self.main_frame, text="Transfer Money", command=self.transfer_window).grid(row=2, column=1, pady=10)
        tk.Button(self.main_frame, text="Check Account Balance", command=self.balance_window).grid(row=3, column=0, pady=10)
        tk.Button(self.main_frame, text="View Transaction History", command=self.history_window).grid(row=3, column=1, pady=10)
        tk.Button(self.main_frame, text="Display All Accounts", command=self.display_accounts).grid(row=4, columnspan=2, pady=10)

    def create_account_window(self):
        window = tk.Toplevel(self.root)
        window.title("Create Account")

        tk.Label(window, text="Account Number").grid(row=0, column=0)
        tk.Label(window, text="Account Holder").grid(row=1, column=0)

        account_number_entry = tk.Entry(window)
        account_holder_entry = tk.Entry(window)

        account_number_entry.grid(row=0, column=1)
        account_holder_entry.grid(row=1, column=1)

        def create_account_action():
            account_number = account_number_entry.get()
            account_holder = account_holder_entry.get()
            message = self.bank.create_account(account_number, account_holder)
            messagebox.showinfo("Create Account", message)
            window.destroy()

        tk.Button(window, text="Create Account", command=create_account_action).grid(row=2, columnspan=2)

    def deposit_window(self):
        window = tk.Toplevel(self.root)
        window.title("Deposit Money")

        tk.Label(window, text="Account Number").grid(row=0, column=0)
        tk.Label(window, text="Amount").grid(row=1, column=0)

        account_number_entry = tk.Entry(window)
        amount_entry = tk.Entry(window)

        account_number_entry.grid(row=0, column=1)
        amount_entry.grid(row=1, column=1)

        def deposit_action():
            account_number = account_number_entry.get()
            amount = float(amount_entry.get())
            message = self.bank.deposit_to_account(account_number, amount)
            messagebox.showinfo("Deposit Money", message)
            window.destroy()

        tk.Button(window, text="Deposit", command=deposit_action).grid(row=2, columnspan=2)

    def withdraw_window(self):
        window = tk.Toplevel(self.root)
        window.title("Withdraw Money")

        tk.Label(window, text="Account Number").grid(row=0, column=0)
        tk.Label(window, text="Amount").grid(row=1, column=0)

        account_number_entry = tk.Entry(window)
        amount_entry = tk.Entry(window)

        account_number_entry.grid(row=0, column=1)
        amount_entry.grid(row=1, column=1)

        def withdraw_action():
            account_number = account_number_entry.get()
            amount = float(amount_entry.get())
            message = self.bank.withdraw_from_account(account_number, amount)
            messagebox.showinfo("Withdraw Money", message)
            window.destroy()

        tk.Button(window, text="Withdraw", command=withdraw_action).grid(row=2, columnspan=2)

    def transfer_window(self):
        window = tk.Toplevel(self.root)
        window.title("Transfer Money")

        tk.Label(window, text="From Account Number").grid(row=0, column=0)
        tk.Label(window, text="To Account Number").grid(row=1, column=0)
        tk.Label(window, text="Amount").grid(row=2, column=0)

        from_account_number_entry = tk.Entry(window)
        to_account_number_entry = tk.Entry(window)
        amount_entry = tk.Entry(window)

        from_account_number_entry.grid(row=0, column=1)
        to_account_number_entry.grid(row=1, column=1)
        amount_entry.grid(row=2, column=1)

        def transfer_action():
            from_account_number = from_account_number_entry.get()
            to_account_number = to_account_number_entry.get()
            amount = float(amount_entry.get())
            message = self.bank.transfer_between_accounts(from_account_number, to_account_number, amount)
            messagebox.showinfo("Transfer Money", message)
            window.destroy()

        tk.Button(window, text="Transfer", command=transfer_action).grid(row=3, columnspan=2)

    def balance_window(self):
        window = tk.Toplevel(self.root)
        window.title("Check Account Balance")

        tk.Label(window, text="Account Number").grid(row=0, column=0)

        account_number_entry = tk.Entry(window)
        account_number_entry.grid(row=0, column=1)

        def check_balance_action():
            account_number = account_number_entry.get()
            account = self.bank.get_account(account_number)
            if account:
                balance = account.get_balance()
                messagebox.showinfo("Account Balance", f"Balance for account {account_number}: {balance}")
            else:
                messagebox.showinfo("Account Balance", "Account not found.")
            window.destroy()

        tk.Button(window, text="Check Balance", command=check_balance_action).grid(row=1, columnspan=2)

    def history_window(self):
        window = tk.Toplevel(self.root)
        window.title("View Transaction History")

        tk.Label(window, text="Account Number").grid(row=0, column=0)

        account_number_entry = tk.Entry(window)
        account_number_entry.grid(row=0, column=1)

        def view_history_action():
            account_number = account_number_entry.get()
            account = self.bank.get_account(account_number)
            if account:
                transactions = account.get_transaction_history()
                history = "\n".join([str(transaction) for transaction in transactions])
                messagebox.showinfo("Transaction History", f"Transaction history for account {account_number}:\n{history}")
            else:
                messagebox.showinfo("Transaction History", "Account not found.")
            window.destroy()

        tk.Button(window, text="View History", command=view_history_action).grid(row=1, columnspan=2)

    def display_accounts(self):
        accounts_summary = str(self.bank)
        messagebox.showinfo("All Accounts", accounts_summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
