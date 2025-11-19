from src.companyaccount import CompanyAccount

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









