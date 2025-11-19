from src.account import Account

import pytest

from src.companyaccount import CompanyAccount


@pytest.fixture
def account():
    return Account()

class TestAccount:

    def test_account_create(self, account):
        assert account.balance == 0
        assert account.history == []

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (20.0, 20.0),
            (-20.0, 0.0),
            (True, 0.0),
        ]
    )
    def test_ingoing_transfer(self, account, amount, expected):
        account.ingoing_transfer(amount)
        assert account.balance == expected

    @pytest.mark.parametrize(
        "balance, amount, expected",
        [
            (20.0, 20.0, 0.0),
            (20.0, -20.0, 20.0),
            (20.0, True, 20.0),
            (0.0, 20.0, 0.0)
        ]
    )
    def test_outgoing_transfer(self, account, balance, amount, expected):
        account.balance = balance
        account.outgoing_transfer(amount)
        assert account.balance == expected

    @pytest.mark.parametrize(
        "balance, amount, fee, expected",
        [
            (30.0, 20.0, 1.0, 9.0),
            (30.0, -20.0, 1.0, 30.0),
            (30.0, True, 1.0, 30.0),
            (0.0, 20.0, 1.0, 0.0),
            (30.0, 20.0, -1.0, 30.0),
            (30.0, 20.0, True, 30.0)
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, fee, expected):
        account.balance = balance
        account.outgoing_express_transfer(amount, fee)
        assert account.balance == expected