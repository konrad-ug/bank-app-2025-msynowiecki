from src.account import Account

import pytest

from src.company_account import CompanyAccount


@pytest.fixture
def account():
    return Account()

class TestAccount:

    def test_account_create(self, account):
        assert account.balance == 0
        assert account.history == []

    @pytest.mark.parametrize(
        "amount, expected, expected_return",
        [
            (20.0, 20.0, True),
            (-20.0, 0.0, False),
            (True, 0.0, False),
        ]
    )
    def test_ingoing_transfer(self, account, amount, expected, expected_return):
        is_accepted = account.ingoing_transfer(amount)
        assert is_accepted == expected_return
        assert account.balance == expected

    @pytest.mark.parametrize(
        "balance, amount, expected, expected_return",
        [
            (20.0, 20.0, 0.0, True),
            (20.0, -20.0, 20.0, False),
            (20.0, True, 20.0, False),
            (0.0, 20.0, 0.0, False),
        ]
    )
    def test_outgoing_transfer(self, account, balance, amount, expected, expected_return):
        account.balance = balance
        is_accepted = account.outgoing_transfer(amount)
        assert is_accepted == expected_return
        assert account.balance == expected

    @pytest.mark.parametrize(
        "balance, amount, fee, expected, expected_return",
        [
            (30.0, 20.0, 1.0, 9.0, True),
            (30.0, -20.0, 1.0, 30.0, False),
            (30.0, True, 1.0, 30.0, False),
            (0.0, 20.0, 1.0, 0.0, False),
            (30.0, 20.0, -1.0, 30.0, False),
            (30.0, 20.0, True, 30.0, False),
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, fee, expected, expected_return):
        account.balance = balance
        is_accepted = account.outgoing_express_transfer(amount, fee)
        assert is_accepted == expected_return
        assert account.balance == expected