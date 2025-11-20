from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.express_fee = 5.0

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10:
            return True
        return False

    def outgoing_express_transfer(self, amount):
        return super().outgoing_express_transfer(amount, self.express_fee)

    def take_loan(self, amount):
        if isinstance(amount, float) and amount > 0 and self.balance >= amount * 2 and -1775.0 in self.history:
            self.balance += amount
            self.history.append(amount)
            return True
        return False