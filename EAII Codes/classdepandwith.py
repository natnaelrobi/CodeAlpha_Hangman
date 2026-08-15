class BankAccount:
    def __init__(self,balance):
        self.balance = balance
    def deposit(self, amount):
        if amount>0:
            self.balance += amount
            print("Deposited amount: ",amount)
        else:
            print("Deposited amount must be positive!")
    def withdraw(self, amount):
        if 0<amount<=self.balance:
            self.balance -= amount
            print("Withdrew amount: ", amount)
        else:
            print("Insufficient balance! or invalid amount")