from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

import pytest


test_account = PersonalAccount("John", "Doe", "99039666673")


@pytest.fixture
def registry():
    return AccountRegistry()

class TestAccountRegistry:


    @pytest.mark.parametrize(
        "account, expected",
        [
            (test_account, [test_account]),
            ("test_account", [])
        ]
    )
    def test_add_account(self, registry, account, expected):
        registry.add_account(account)
        assert registry.accounts == expected


    @pytest.mark.parametrize(
        "pesel, accounts, expected",
        [
            ("99039666673", [test_account], test_account),
            ("99039666672", [test_account], None),
        ]
    )
    def test_find_account(self, registry, pesel, accounts, expected):
        registry.accounts = accounts
        assert registry.find_account(pesel) == expected


    def test_get_accounts(self, registry):
        assert registry.get_accounts() == []
        registry.add_account(test_account)
        assert registry.get_accounts() == [test_account]


    def test_get_accounts_number(self, registry):
        assert registry.get_accounts_number() == 0
        registry.add_account(test_account)
        assert registry.get_accounts_number() == 1
