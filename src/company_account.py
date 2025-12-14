from src.account import Account
import requests
import datetime

url = "https://wl-test.mf.gov.pl/api/search/nip"


class CompanyAccount(Account):

    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        self.nip = nip
        self.express_fee = 5.0

        if self.is_nip_valid(nip):
            if not self.does_nip_exist(nip):
                raise ValueError("Company not registered!!")


    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10


    def does_nip_exist(self, nip):
        response = requests.get(f'{url}/{nip}?date={datetime.date.today()}')
        data = response.json()

        if data["result"]["subject"]["statusVat"]:
            if data["result"]["subject"]["statusVat"] == "Czynny":
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