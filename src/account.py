class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def ingoing_transfer(self, amount):
        if isinstance(amount, float) and amount > 0.0:
            self.balance += amount
            self.history.append(amount)

    def outgoing_transfer(self, amount):
        if isinstance(amount, float) and amount > 0.0 and self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)

    def outgoing_express_transfer(self, amount, fee):
        if isinstance(amount, float) and isinstance(fee, float) and amount > 0.0 and fee >= 0.0 and self.balance - amount - fee > -fee:
            self.balance -= amount + fee
            self.history.append(-amount)
            self.history.append(-fee)

