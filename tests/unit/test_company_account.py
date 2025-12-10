from src.company_account import CompanyAccount

import pytest

@pytest.fixture
def account():
    return CompanyAccount("SupCompany", "1021010102")

class TestCompanyAccount:

    @pytest.mark.parametrize(
        "balance, amount, expected",
        [
            (0.0, 10.0, 0.0),
            (20.0, -10.0, 20.0),
            (20.0, True, 20.0),
            (20.0, 10.0, 5.0),
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, expected):
        account.ingoing_transfer(balance)
        account.outgoing_express_transfer(amount)
        assert account.balance == expected


    @pytest.mark.parametrize(
        "history, balance, amount, expected, expected_value",
        [
            ([10.0, -1775.0, 10.0], 20.0, 10.0, 30.0, True),
            ([10.0, 10.0, 10.0], 20.0, 10.0, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, 15.0, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, True, 20.0, False),
            ([10.0, -1775.0, 10.0], 20.0, -10.0, 20.0, False)
        ]
    )
    def test_take_loan(self, account, balance, history, amount, expected, expected_value):
        account.history = history
        account.balance = balance
        result = account.take_loan(amount)
        assert result == expected_value
        assert account.balance == expected








