from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "99039666673")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "99039666673"
        assert account.balance == 0.0
        assert account.promotion_code == "Invalid"

    def test_short_pesel(self):
        account = Account("John", "Doe", "9903966667")
        assert account.pesel == "Invalid"

    def test_long_pesel(self):
        account = Account("John", "Doe", "990396666734")
        assert account.pesel == "Invalid"

    def test_pesel_non_digit(self):
        account = Account("John", "Doe", None)
        assert account.pesel == "Invalid"

    def test_prom_code_valid(self):
        account = Account("John", "Doe", "59039666673", "PROM_XYZ")
        assert account.balance == 50.0
        assert account.promotion_code == "PROM_XYZ"

    def test_prom_code_valid_but_age(self):
        account = Account("John", "Doe", "99039666673", "PROM_XYZ")
        assert account.balance == 0.0
        assert account.promotion_code == "PROM_XYZ"

    def test_prom_code_invalid(self):
        account = Account("John", "Doe", "99039666673", "PRM_XYZ")
        assert account.balance == 0.0
        assert account.promotion_code == "Invalid"

