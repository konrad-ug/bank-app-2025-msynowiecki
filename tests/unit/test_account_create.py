from src.personalaccount import PersonalAccount
from src.companyaccount import CompanyAccount


class TestPersonalAccount:

    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "99039666673"
        assert account.balance == 0.0
        assert account.promotion_code == "Invalid"

    def test_short_pesel(self):
        account = PersonalAccount("John", "Doe", "9903966667")
        assert account.pesel == "Invalid"

    def test_long_pesel(self):
        account = PersonalAccount("John", "Doe", "990396666734")
        assert account.pesel == "Invalid"

    def test_pesel_non_digit(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.pesel == "Invalid"

    def test_prom_code_valid(self):
        account = PersonalAccount("John", "Doe", "59039666673", "PROM_XYZ")
        assert account.balance == 50.0
        assert account.promotion_code == "PROM_XYZ"

    def test_prom_code_valid_but_age(self):
        account = PersonalAccount("John", "Doe", "99039666673", "PROM_XYZ")
        assert account.balance == 0.0
        assert account.promotion_code == "PROM_XYZ"

    def test_prom_code_invalid(self):
        account = PersonalAccount("John", "Doe", "99039666673", "PRM_XYZ")
        assert account.balance == 0.0
        assert account.promotion_code == "Invalid"

    def test_ingoing_transfer_invalid_amount(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.ingoing_transfer(-20.0)
        assert account.balance == 0.0
        
    def test_ingoing_transfer_invalid_type(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.ingoing_transfer('20')
        assert account.balance == 0.0


    def test_ingoing_transfer_valid(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.ingoing_transfer(20.0)
        assert account.balance == 20.0

    def test_outgoing_transfer_invalid_amount(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.outgoing_transfer(-20.0)
        assert account.balance == 0.0
        
    def test_outgoing_transfer_invalid_type(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.outgoing_transfer('20')
        assert account.balance == 0.0

    def test_outgoing_transfer_invalid_balance(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        assert account.balance == 0.0
        account.outgoing_transfer(20.0)
        assert account.balance == 0.0

    def test_outgoing_transfer_valid(self):
        account = PersonalAccount("John", "Doe", "99039666673")
        account.ingoing_transfer(30.0)
        assert account.balance == 30.0
        account.outgoing_transfer(20.0)
        assert account.balance == 10.0

class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("SupCompany", "1021010102")
        assert account.name == "SupCompany"
        assert account.nip == "1021010102"

    def test_nip_short(self):
        account = CompanyAccount("SupCompany", "102101010")
        assert account.nip == "Invalid"

    def test_nip_long(self):
        account = CompanyAccount("SupCompany", "10210101022")
        assert account.nip == "Invalid"





        



