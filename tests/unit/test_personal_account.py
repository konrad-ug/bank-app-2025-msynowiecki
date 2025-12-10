from src.personal_account import PersonalAccount

import pytest

@pytest.fixture
def account():
    return PersonalAccount("John", "Doe", "99039666673")

class TestPersonalAccount:

    @pytest.mark.parametrize(
        "balance, amount, expected",
        [
            (0.0, 10.0, 0.0),
            (20.0, -10.0, 20.0),
            (20.0, True, 20.0),
            (20.0, 10.0, 9.0),
        ]
    )
    def test_outgoing_express_transfer(self, account, balance, amount, expected):
        account.ingoing_transfer(balance)
        account.outgoing_express_transfer(amount)
        assert account.balance == expected

    @pytest.mark.parametrize(
        "history, amount, expected, expected_value",
        [
            ([30.0, 30.0, 30.0, 30.0, 30.0], 10.0, 10.0, True),
            ([10.0, 10.0, 10.0, 10.0, 10.0], -500.0, 0.0, False),
            ([130.0, 30.0, 30.0, -30.0, -30.0, -30.0], 10.0, 0.0, False),
            ([30.0], 10.0, 0.0, False)
        ]
    )
    def test_submit_for_loan(self, account, history, amount, expected, expected_value):
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_value
        assert account.balance == expected