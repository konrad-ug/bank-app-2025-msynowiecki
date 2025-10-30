class Account:
    def __init__(self):
        self.balance = 0.0

    def ingoing_transfer(self, amount):
        if isinstance(amount, float) and amount > 0.0:
            self.balance += amount


    def outgoing_transfer(self, amount):
        if isinstance(amount, float) and amount > 0.0 and self.balance > amount:
            self.balance -= amount