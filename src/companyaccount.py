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