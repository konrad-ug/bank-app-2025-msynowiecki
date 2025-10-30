from src.account import Account

class PersonalAccount(Account):

    def __init__(self, first_name, last_name, pesel, promotion_code="Invalid"):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50.0 if self.is_promotion_code_valid(promotion_code) and self.is_born_after_1960(pesel) else 0.0
        self.promotion_code = promotion_code if self.is_promotion_code_valid(promotion_code) else "Invalid"
        self.express_fee = 1.0

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit():
            return True
        return False

    def is_promotion_code_valid(self, promotion_code):
        if isinstance(promotion_code, str) and promotion_code.startswith("PROM_") and len(promotion_code) == 8:
            return True
        return False

    def is_born_after_1960(self, pesel):
        if int(pesel[2:4]) <= 12 and int(pesel[:2]) < 60:
            return True
        return False

    def outgoing_express_transfer(self, amount):
        return super().outgoing_express_transfer(amount, self.express_fee)


