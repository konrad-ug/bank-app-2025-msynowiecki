from src.company_account import CompanyAccount
from src.personal_account import PersonalAccount

import pytest

@pytest.mark.parametrize(
    "first_name, last_name, pesel, expected",
    [
        ("John", "Doe", "99039666673", "99039666673"),
        ("John", "Doe", "9903966667X", "Invalid"),
        ("John", "Doe", "990396666732", "Invalid"),
        ("John", "Doe", "9903966667", "Invalid"),
        ("John", "Doe", True, "Invalid")
    ]
)
def test_personal_account_creation(first_name, last_name, pesel, expected):
    account = PersonalAccount(first_name, last_name, pesel)
    assert account.first_name == first_name
    assert account.last_name == last_name
    assert account.pesel == expected


@pytest.mark.parametrize(
    "first_name, last_name, pesel, promotion_code, expected, expected_code",
    [
        ("John", "Doe", "59039666673", "PROM_XYZ", 50.0, "PROM_XYZ"),
        ("John", "Doe", "99039666673", "PROM_XYZ", 0.0, "PROM_XYZ"),
        ("John", "Doe", "99039666673", "PROM_XY", 0.0, "Invalid"),
    ]
)
def test_personal_account_creation(first_name, last_name, pesel, promotion_code, expected, expected_code):
    account = PersonalAccount(first_name, last_name, pesel, promotion_code)
    assert account.balance == expected
    assert account.promotion_code == expected_code


def test_is_pesel_valid_direct():
    account = PersonalAccount("John", "Doe", "99039666673")
    assert account.is_pesel_valid("123") is False


@pytest.mark.parametrize(
    "name, nip, expected",
    [
        ("SupCompany", "1021010102", "1021010102"),
        ("SupCompany", "10210101022", "Invalid"),
        ("SupCompany", "102101010", "Invalid"),
        ("SupCompany", True, "Invalid"),
    ]
)
def test_company_account_creation(mocker, name, nip, expected):
    mocker.patch("src.company_account.CompanyAccount.does_nip_exist", return_value=True)

    account = CompanyAccount(name, nip)

    assert account.name == name
    assert account.nip == expected


def test_company_account_create(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}

    mocker.patch("requests.get", return_value=mock_response)

    account = CompanyAccount("Test Company", "1234567890")

    assert account.name == "Test Company"
    assert account.nip == "1234567890"


def test_company_account_create_invalid_nip(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "result": {
            "subject": {
                "statusVat": None
            }
        }
    }

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(ValueError):
        CompanyAccount("Fake Company", "1234567890")
