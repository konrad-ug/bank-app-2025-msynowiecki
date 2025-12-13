from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

import pytest


test_account = PersonalAccount("John", "Doe", "99039666673")
test_new_account = PersonalAccount("Joe", "Doe", "99039666673")
test_pesel = "99039666673"


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
        "account, pesel, expected",
        [
            (test_account, test_pesel, []),
            (test_account, "test_pesel", [test_account])
        ]
    )
    def test_remove_account(self, registry, account, pesel, expected):
        registry.add_account(account)
        registry.remove_account(pesel)

        if expected:
            assert registry.accounts[0].pesel == expected[0].pesel
            assert registry.accounts[0].first_name == expected[0].first_name
            assert registry.accounts[0].last_name == expected[0].last_name
        else:
            assert registry.accounts == []

    @pytest.mark.parametrize(
        "account, pesel, new, expected",
        [
            (test_account, test_pesel, test_new_account, [test_new_account]),
            (test_account, "test_pesel", test_new_account, [test_account]),
            (test_account, test_pesel, "test_new_account", [test_account])
        ]
    )
    def test_update_account(self, registry, account, pesel, new, expected):
        registry.add_account(account)
        registry.update_account(pesel, new)
        
        if expected:
            assert registry.accounts[0].pesel == expected[0].pesel
            assert registry.accounts[0].first_name == expected[0].first_name
            assert registry.accounts[0].last_name == expected[0].last_name
        else:
            assert registry.accounts == []

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
